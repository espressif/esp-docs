// Import Wokwi client library
import { APIClient, MessagePortTransport } from 'wokwi-client-js';

(function() {
  "use strict";

  // Store API clients and state for each iframe
  var iframeClients = new WeakMap();
  var iframePaused = new WeakMap();
  var iframeVisible = new WeakMap();

  // Check if iframe is Wokwi with API enabled
  function isWokwiApiIframe(iframe) {
    if (!iframe || !iframe.src) return false;
    try {
      var url = new URL(iframe.src);
      return url.hostname.includes('wokwi.com') && url.searchParams.has('api');
    } catch (e) {
      return false;
    }
  }

  // Determine if simulation should be running
  function shouldSimulationRun(iframe) {
    var panel = iframe.closest('.wokwi-panel');
    var isActiveTab = !panel || panel.getAttribute('data-active') === 'true';
    var isScrolledIntoView = iframeVisible.get(iframe) !== false;
    var isPageVisible = !document.hidden;
    
    return isActiveTab && isScrolledIntoView && isPageVisible;
  }

  // Update simulation state based on visibility
  function updateSimulationState(iframe) {
    var client = iframeClients.get(iframe);
    if (!client) return;

    var shouldRun = shouldSimulationRun(iframe);
    var isPaused = iframePaused.get(iframe) || false;

    if (shouldRun && isPaused) {
      client.simResume().then(function() {
        iframePaused.set(iframe, false);
      }).catch(function(err) {
        console.error('Failed to resume simulation:', err);
      });
    } else if (!shouldRun && !isPaused) {
      client.simPause().then(function() {
        iframePaused.set(iframe, true);
      }).catch(function(err) {
        console.error('Failed to pause simulation:', err);
      });
    }
  }

  // Setup Wokwi API client for iframe
  function setupWokwiClient(iframe) {
    if (!isWokwiApiIframe(iframe)) return;
    if (iframeClients.has(iframe)) return;

    var messageHandler = function(event) {
      if (!event.origin || !event.origin.includes('wokwi.com')) return;
      if (!event.data || !event.data.port) return;
      if (event.source !== iframe.contentWindow) return;
      
      try {
        var transport = new MessagePortTransport(event.data.port);
        var client = new APIClient(transport);
        
        iframeClients.set(iframe, client);
        iframePaused.set(iframe, false);

        client.connected.then(function() {
          // Check initial state
          setTimeout(function() {
            updateSimulationState(iframe);
          }, 500);
        }).catch(function(err) {
          console.error('Failed to connect to Wokwi API:', err);
        });

        window.removeEventListener('message', messageHandler);
      } catch (err) {
        console.error('Error setting up Wokwi client:', err);
      }
    };

    window.addEventListener('message', messageHandler);
  }

  // Initialize all Wokwi iframes
  function initializeWokwiIframes() {
    document.querySelectorAll('iframe').forEach(function(iframe) {
      if (isWokwiApiIframe(iframe)) {
        setupWokwiClient(iframe);
        iframe.addEventListener('load', function() {
          setupWokwiClient(iframe);
        });
      }
    });
  }

  // Track iframe visibility with Intersection Observer
  function setupIntersectionObserver() {
    if (typeof IntersectionObserver === 'undefined') return;

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var iframe = entry.target;
        if (!isWokwiApiIframe(iframe)) return;

        var isVisible = entry.isIntersecting && entry.intersectionRatio > 0.5;
        var wasVisible = iframeVisible.get(iframe);

        if (isVisible !== wasVisible) {
          iframeVisible.set(iframe, isVisible);
          updateSimulationState(iframe);
        }
      });
    }, {
      threshold: [0, 0.5, 1.0],
      rootMargin: '50px'
    });

    document.querySelectorAll('iframe').forEach(function(iframe) {
      if (isWokwiApiIframe(iframe)) {
        observer.observe(iframe);
        iframeVisible.set(iframe, false);
      }
    });

    return observer;
  }

  // Pause/resume on browser tab switch
  function setupPageVisibilityHandler() {
    if (typeof document.hidden === 'undefined') return;

    document.addEventListener('visibilitychange', function() {
      document.querySelectorAll('iframe').forEach(function(iframe) {
        if (isWokwiApiIframe(iframe) && iframeClients.has(iframe)) {
          updateSimulationState(iframe);
        }
      });
    });
  }

  // Tab switching functionality
  function setActionsVisibility(root) {
    var active = root.querySelector('.wokwi-panel[data-active="true"]');
    var hasWokwi = !!(active && active.getAttribute('data-viewer-url'));
    
    var fullscreenBtn = root.querySelector('.wokwi-fullscreen-btn[data-wokwi-only="true"]');
    if (fullscreenBtn) {
      fullscreenBtn.style.display = hasWokwi ? "" : "none";
    }
  }

  function updateLaunchpadUrl(root) {
    var launchpadBtn = root.querySelector('.wokwi-launchpad-btn');
    if (!launchpadBtn) return;

    var baseHref = launchpadBtn.getAttribute('data-base-href');
    if (baseHref) {
      launchpadBtn.setAttribute('href', baseHref);
    }
  }

  function onTabClick(e) {
    var btn = e.target.closest('.wokwi-tab');
    if (!btn) return;
    var root = btn.closest('.wokwi-tabs');
    if (!root) return;

    // Pause iframe in previously active panel
    var previousPanel = root.querySelector('.wokwi-panel[data-active="true"]');
    if (previousPanel) {
      var previousIframe = previousPanel.querySelector('iframe');
      if (previousIframe && isWokwiApiIframe(previousIframe)) {
        updateSimulationState(previousIframe);
      }
    }

    // Update tab selection
    root.querySelectorAll('.wokwi-tab').forEach(function(b) {
      b.setAttribute('aria-selected', String(b === btn));
    });

    // Update panel visibility
    var id = btn.getAttribute('data-target');
    root.querySelectorAll('.wokwi-panel').forEach(function(p) {
      p.dataset.active = String(p.id === id);
    });

    updateLaunchpadUrl(root);
    setActionsVisibility(root);

    // Resume iframe in newly active panel
    var activePanel = root.querySelector('.wokwi-panel[data-active="true"]');
    if (activePanel) {
      var activeIframe = activePanel.querySelector('iframe');
      if (activeIframe && isWokwiApiIframe(activeIframe)) {
        if (!iframeClients.has(activeIframe)) {
          setTimeout(function() {
            setupWokwiClient(activeIframe);
          }, 100);
        } else {
          updateSimulationState(activeIframe);
        }
      }
    }
  }

  function buildModal(url) {
    var modal = document.createElement('div');
    modal.className = 'wokwi-modal';
    modal.innerHTML = 
      '<button class="wokwi-modal__close" title="Close">✕</button>' +
      '<div class="wokwi-modal__inner">' +
      '<iframe class="wokwi-modal__frame" allowfullscreen></iframe>' +
      '</div>';

    modal.querySelector('iframe').src = url;

    function closeModal() {
      try { 
        document.body.removeChild(modal); 
      } catch (_) {}
    }

    modal.addEventListener('click', function(ev) {
      if (ev.target.classList.contains('wokwi-modal')) {
        closeModal();
      }
    });

    modal.querySelector('.wokwi-modal__close').addEventListener('click', closeModal);

    document.addEventListener('keydown', function escHandler(ev) {
      if (ev.key === 'Escape') {
        closeModal();
        document.removeEventListener('keydown', escHandler);
      }
    });

    return modal;
  }

  function openFullscreen(root) {
    var panel = root.querySelector('.wokwi-panel[data-active="true"]');
    var url = panel ? panel.getAttribute('data-viewer-url') : null;
    
    if (!url) {
      var iframe = root.querySelector('iframe');
      if (iframe && iframe.src) url = iframe.src;
    }
    
    if (url) {
      document.body.appendChild(buildModal(url));
    }
  }

  function onFullscreenClick(e) {
    var btn = e.target.closest('.wokwi-fullscreen-btn');
    if (!btn) return;
    
    e.preventDefault();
    var root = btn.closest('.wokwi-tabs') || btn.closest('.wokwi-frame');
    if (root) {
      openFullscreen(root);
    }
  }

  // Event listeners
  document.addEventListener('click', onTabClick);
  document.addEventListener('click', onFullscreenClick);

  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.wokwi-tabs').forEach(function(root) {
      setActionsVisibility(root);
      updateLaunchpadUrl(root);
    });
    
    // Initialize auto-pause/resume functionality
    initializeWokwiIframes();
    setupIntersectionObserver();
    setupPageVisibilityHandler();

    // Watch for dynamically added iframes
    if (typeof MutationObserver !== 'undefined') {
      var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          mutation.addedNodes.forEach(function(node) {
            if (node.nodeType === 1) {
              if (node.tagName === 'IFRAME' && isWokwiApiIframe(node)) {
                setupWokwiClient(node);
              }
              var iframes = node.querySelectorAll && node.querySelectorAll('iframe');
              if (iframes) {
                iframes.forEach(function(iframe) {
                  if (isWokwiApiIframe(iframe)) {
                    setupWokwiClient(iframe);
                  }
                });
              }
            }
          });
        });
      });
      
      observer.observe(document.body, { childList: true, subtree: true });
    }
  });
})();
