# Goalboost
Goalboost is a time and billing application written using Python, Flask, and MongoDb.  It is employee owned source, not open source -- see the [license](LICENSE.md).

# Getting Started.
Well, you'll need Python 3 and MongoDb for starters.  You can clone the code according to the license, but to work on it you'll need to get our environment settings, which contain the security-sensitive stuff.  Ping [John Lockwood](http://github.com/JohnLockwood) if you're interested.

# Hours 
We keep track of our hours in [docs/hours.json](docs/hours.json)

# Time and Billing App (Specification -- First Try)

## Some Ideas / Competitors:

* [RocketMatter](https://www.rocketmatter.com/law-office-management-software/)
* [GetHarvest](https://www.getharvest.com)
* [Toggle](https://toggl.com)

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


