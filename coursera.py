#!/usr/bin/env python

import requests
import webapp2
import os
import jinja2
import datetime
import calendar
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'])
DEBUG = True

class ListCourses(webapp2.RequestHandler):

    def determine_date(self, latest):
        day = latest['start_day']
        month = latest['start_month']
        year = latest['start_year']
        if year is not None and year != '':
            if month is not None and month != '':
                month = calendar.month_name[month]
                if day is not None and day != '':
                    date = '%s %s, %s' % (day, month, year)
                else:
                    date = '%s %s' % (month, year)
            else:
                date = str(year)
        else:
            date = ''
        return date


    def get(self):
        api_url = "https://www.coursera.org/maestro/api/topic/list"
        api = requests.get(api_url)
        js = api.json()
        courses = []
        for course in js:
            image = course['large_icon']
            name = course['name']
            instructor = course['instructor']
            short_description = course['short_description']
            preview_link = course['preview_link']
            if len(course['courses']) > 0:
                latest_offering = course['courses'][-1]
                duration = latest_offering['duration_string']
                date = self.determine_date(latest_offering)
            else:
                date = None
                duration = None
            if duration is not None and duration != '':
                duration += " long"
            universities = []
            for university in course[u'universities']:
                u_logo = university['logo']
                u_description = university['description']
                u_name = university['name']
                u_home_link = university['home_link']
                u_website = university['website']
                universities.append({'u_name':u_name, 'u_logo':u_logo,
                                        'u_description':u_description,
                                        'u_home_link':u_home_link,
                                        'u_website':u_website})

            courses.append({'name':name,'image':image, 'instructor':instructor,
                            'short_description':short_description,
                            'preview_link':preview_link,
                            'start_date':date,
                            'duration':duration, 'universities':universities})

        template_values = {
                'courses': courses
        }

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.out.write(template.render(template_values))

application = webapp2.WSGIApplication([('/', ListCourses),
                              ], debug=DEBUG)
