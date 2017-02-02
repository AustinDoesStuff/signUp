#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

def BuildPage(username, email, userError, passError,conPassError, emailError):
    header = """
    <html>
        <head>
        </head>
        <body>
    """

    heading = "<h1>Sign up plz</h1><br><br>"

    mainBody = """
        <form action = '/' method='post'>
            <label>Username:<input type='text' name='user' value = '{username}' required></input></label><span> {user}</span><br><br>
            <label>Password:<input type='password' name='pass' required></input></label><span> {password}</span><br><br>
            <label>Confirm Password:<input type='password' name='confirmPass' required></input></label><span> {confirmPassword}</span><br><br>
            <label>Email:<input type='text' name='email' value = '{displayEmail}'></input></label><span> {email}</span><br><br>
            <br>
            <input type='submit'>
        </form>
    """.format(username = username, displayEmail = email, user = userError, password = passError,confirmPassword = conPassError, email = emailError)
    footer = """
        </body>
    </html>
    """
    page = header + heading + mainBody + footer
    return page


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = BuildPage("","","","","","")
        self.response.write(content)

    def post(self):

        def valid(regex, testCase):
            return regex.match(testCase)

        username = cgi.escape(self.request.get('user'))
        password = cgi.escape(self.request.get('pass'))
        confirmPassword = cgi.escape(self.request.get('confirmPass'))
        email = cgi.escape(self.request.get('email'))

        userRE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        passRE = re.compile(r"^.{3,20}$")
        emailRE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        userMessage = ""
        passMessage = ""
        emailMessage = ""
        confirmPassMessage = ""

        if valid(userRE, username) == None:
            userMessage = "Hey, that's not a valid username, idiot"
        if valid(passRE, password) == None:
            passMessage = "Your password sucks, try again"
        if valid(emailRE, email) == None:
            emailMessage = "You broke the email, dummy"
        if len(email) < 1:
            emailMessage = ""
        if password != confirmPassword:
            confirmPassMessage = "They didn't match. Learn to type."

        if len(userMessage) > 1 or len(passMessage) > 1 or len(emailMessage) > 1 or password != confirmPassword:
            self.response.write(BuildPage(username, email, userMessage,passMessage, confirmPassMessage, emailMessage))
        else:
            self.redirect('/welcome?username=' + username)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user = self.request.get("username")
        self.response.write("Thanks for logging in, " + user + "!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
