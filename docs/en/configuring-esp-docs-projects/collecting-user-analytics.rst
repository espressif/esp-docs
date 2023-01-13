Collecting User Analytics
=========================

`Google Analytics <https://www.google.com/analytics/>`_ is a free web analytics service offered by Google that provides data for your website, such as the number of visitors to your site, where they came from, and what pages they viewed. Additionally, you can track the active user and conversion rate. The service is widely used by website owners and marketers to track the performance of their website and improve its performance.

Enabling Google Analytics for Your Project
------------------------------------------

To enable Google Analytics for your project:

1. Obtain **Tracking ID** by sending your request to Documentation Team Manager.
2. Go to ``docs/conf_common.py``, and add the following code to it. The ``YOUR_TRACKING_ID`` should be changed to the obtained **Tracking ID** from the previous step.

    ::

        # add Tracking ID for Google Analytics

        google_analytics_id = 'YOUR_TRACKING_ID'


3. Once you've added the **Tracking ID** to your project, you will need to wait for some time before data will appear on the Google Analytics platform.


Viewing Google Analytics Data or Reports
----------------------------------------

To view Google Analytics data or reports:

1. Create a `Google account <https://accounts.google.com/signin>`_ if you don't already have one, then sign up for Google Analytics.
2. Gain access to data or reports by sending your Google account to Documentation Team Manager.
3. Log in to `Google Analytics <https://www.google.com/analytics/>`_ and view reports.


See more descriptions in `Google Analytics for Beginners <https://analytics.google.com/analytics/academy/course/6>`_.