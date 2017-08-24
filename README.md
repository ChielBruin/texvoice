# texvoice
Create professional and consistent-looking invoices from the exports of your timekeeping tools.

This tool inserts the exported data in a Latex template and compiles it to a `.pdf` file.
This way all invoices follow the exact same styling and this styling is fully configurable to your personal preference.  
By creating your own template a custom invoice can be created that fits your company (some Latex knowledge is required for this).

## Supported timekeeping tools
- [Timesheet](https://play.google.com/store/apps/details?id=com.rauscha.apps.timesheet) [Dutch version]

Currently only the Dutch version is supported, due to a language specific `.csv`. format.
I plan to make the tool more flexible by making a generic way to parse `.csv` exports in many formats and maybe support for different formats (See the roadmap).

## Template structure
`texvoice` uses Latex templates for building the invoices. 
These templates contain placeholder macros that are subsituted with the timekeeping data when creating the invoice.
A template file is a `.zip` archive containing all the files that are needed by the template file itself.
This template file is simply called `template.tex`. The archive should also contain a `.pdf` example of the template, making the following structure.

```
MyTemplate.zip
     |
     | template.tex
     | example.pdf
```

### Keywords
The template can contain several keywords that are substituted for values from the data when creating the invoices.
These keywords belong to one of two groups, either related to a single task entry or globally to the entire invoice/project.  
Note that the hourly wage is task-data and therefore not global. 
In the case of a wage that is the same for the entire project, the (global) average wage can be used as this should be equal.

_Task data:_
- `\description`  
 The description of this task
- `\hours`  
 The amount of hours spent on this task
- `\price`  
 The hourly wage for this task
- `\total`  
 The total price of this task (= time * price)
- `\begin{hourListing} <format> \end{hourListing}`  
 The line(s) contained in this block are created for each entry in the input data.  
 In the `<format>`, previously mentioned keywords are substituted
 
_Project data:_
- `\clientName`  
 The (company) name of the client
- `\projectID`  
 The ID given to this project
- `\invoiceID`  
 The ID of this invoice as a method of distinguishing different invoices for the same client
- `\projectDescription`  
 The description of the project
- `\avgPrice`  
 The average hourly wage paid on all tasks
- `\priceSubtotal`  
 The price excluding VAT
- `\VAT`  
 The VAT percentage
- `\priceVAT`  
 The added price by VAT
- `\priceTotal`  
 The toal price including VAT
 
 ## Roadmap
 - Improve the architecture of the code  
  The current code is a (working) proof of concept, but not very well written
 - Add support for all `.csv` exports  
  Make use of layout configs to make them work with many tools without writing any code
 - Add some more layouts
 - Add support for multipage invoices
 
 ## Contributions
 Feel free to contribute new templates or add support for more timekeeping tools
