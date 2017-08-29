# texvoice
Create professional and consistent-looking invoices from the exports of your timekeeping tools.

This tool inserts the exported data in a Latex template and compiles it to a `.pdf` file.
This way all invoices follow the exact same styling and this styling is fully configurable to your personal preference.  
By creating your own template a custom invoice can be created that fits your company (some Latex knowledge is required for this).

## Supported timekeeping tools
- [Timesheet](https://play.google.com/store/apps/details?id=com.rauscha.apps.timesheet) [Dutch version]

Currently only the Dutch version is supported, due to a language specific `.csv`. format.
By the usage of CSV config files, it is easy to add support for a new tool that exports CSV files.

## Template structure
`texvoice` uses Latex templates for building the invoices. 
These templates contain placeholder macros that are subsituted with the timekeeping data when creating the invoice.
A template file is a `.zip` archive containing all the files that are needed by the template file itself.
This template file is simply called `template.tex`. Furthermore, the archive should contain a file called `VERSION`. 
This file contains the versions of texvoice for which the template is created and therefore is compatible.
The archive should also contain a `example.pdf` example of the template, making the following structure.

```
MyTemplate.zip
     |
     | VERSION
     | template.tex
     | example.pdf
```

### Keywords
The template can contain several keywords that are substituted for values from the data when creating the invoices.
These keywords belong to one of two groups, either related to a single task entry or globally to the entire invoice/project.  
Note that some keywords related to pricing are in both groups, this makes the substituted values dependend on the current scope of the compiler.

_Task data:_
- `\description`  
 The description of this task
- `\duration`  
 The amount of hours spent on this task
- `\wage`  
 The hourly wage for this task
- `\subtotal`  
 The total price of this task excluding VAT (= time * price)
- `\total`  
 The total price of this task including VAT (= time * price + VAT)
- `\vatPercentage`  
 The VAT percentage on this tasks price
- `\vat`  
 The total VAT added on this tasks price
 
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
- `\wage`  
 The average hourly wage paid on all tasks
 Note: You dhould only use this when the hourly wage is the same for all tasks, or things might get confusing for the client
- `\duration`  
 The total duration of all tasks
- `\subtotal`  
 The total price excluding VAT
- `\vatPercentage`  
 The VAT percentage
 Note: You dhould only use this when the VAT is the same for all tasks, or things might get confusing for the client
- `\vat`  
 The added price by VAT
- `\total`  
 The total price including VAT
 
 ## Roadmap
 - Add some more layouts
 - Add support for multipage invoices
 - Better error handling
 
 ## Contributions
 Feel free to contribute new templates or add support for more timekeeping tools
