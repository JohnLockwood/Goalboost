# Goalboost
Goalboost is a time and billing application written in Python and Flask.  It is employee owned source, not open source -- see the [license](LICENSE.md).  

# We've moved.  
We have moved to a private Bitbucket repository and made a fair number of changes recently, including moving to SQLAlchemy from MongoDb. If you'd like to work with us, please send send a request for access by email at CodeSolid@yahoogroups.com.  We are actively encouraging new contributors.

# Other Issues
## Free Love
If you'd care to encourage us without doing much work, we appreciate all stars and fork requests.  Sure, a fork is pretty much symbolic at this point -- but it strikes a blow for freedom! ;)

## Hours
We're tracking the time we spent on the project in Goalboost now rather than in hours.name.json.  Don't worry if you've already logged hours -- we'll make sure they're moved  into Goalboost and retained as we work through our schema changes.

<!--
# Getting Started.

We'll need to rework that section and retest a bit once the 
You'll need Python 3 and MongoDb installed, as well as PIP3 if that doesn't come with your python3 distribution.  Once you have these, follow these steps:
Make sure the mongo service is running (mongod)
To install the dependencies run "pip3 install -r /path/to/requirements.txt" (requirements.txt is in the source code folder root).
Once you've done this you should be able to run the server in the source code root with the following command:

python3 manage.py runserver_debug

At this point you if all goes well you'll have a server running at http://localhost:5000.  Because we're running mongo no datbase setup is needed other than
to run the server -- collections will be created as we go along.

# Hours 
We keep track of our hours in [docs/hours.json](docs/hours.json)

# Time and Billing App (Specification -- First Try)

## Some Ideas / Competitors:

* [RocketMatter](https://www.rocketmatter.com/law-office-management-software/)
* [GetHarvest](https://www.getharvest.com)
* [Toggle](https://toggl.com)
* [Bill4Time](http://www.bill4time.com)
* [Foundation Time and Materials](http://www.foundationsoft.com/construction-software/time-material/) - construction
* [Chrometa](http://www.chrometa.com/)

See also the time and billing section of [this article](http://www.americanbar.org/publications/law_practice_magazine/2011/september_october/popular_cloud_computing_services_for_lawyers.html) re [Bill4Time](http://www.bill4time.com) and [Chrometa](http://www.chrometa.com/).

## Concepts:

* Team -- this is our customer's employees or associates, the folks doing the billing
* People -- "Subclasses" (conceptually) are TeamPeople (aka Users) or ClientPeople.  The difference will be modeled this way:
* 	"userCredentials" will be none on non-users, or will contain userCredentials for users.
* Client -- This is a company (or person) which we bill for services
* Projects / Matters - a body of work that can be billed separately or used for tracking.  Related to Clients / ClientPeople.
* Timers (Description, plus 1-N dates and times.  Second precision but may need rounding rules for invoices?)
* "Billable" -- can be a project, a company, or a person.  
* Invoices, which consist of invoice lines and reference a billable.
* InvoiceItem:
	* Is either a service or expense
	* Assumption for services is rate * hours = amount.  May elect to show hours and rates on invoice or not.
	* Contains a description of task (timer description), a short service title (e.g senior partner, designer, paralegal, etc.)
	* Edit form contains simple checkbox to exclude or not, edit controls for everything else to adjust (hours etc.)
* Rates:
	* Are either by Billable (client, project etc.) or by ServiceTitle (Senior Partner, Senior Partner Courtroom, etc.), or both.
-->