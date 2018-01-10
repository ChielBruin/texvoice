# texvoice
Create professional and consistent-looking invoices from the exports of your timekeeping tools using Latex templates.

This tool inserts the exported data in the selected Latex template and compiles it to a `.pdf` file.
This way all invoices follow the exact same styling and this styling is fully configurable to your personal preference.  
By creating your own template a custom invoice can be created that fits your company (some Latex knowledge is required for this).

> ### Texvoice is currently being improved to its version 2.0, see the roadmap for more information

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
The archive should also contain a `example.pdf` example of the template, making the following structure:

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
As the second group contains accumulations of many entries, they might not contain sensible data. 
For example the description field remains empty and the VAT percentage becomes a weighted average.
The two groups also contain two scoping levels. The first (local) level applies to either the hours, the expenses or the travel costs. The global scope uses the totals of the three local scopes.

``` Latex
% Listing for each data entry
\begin{texvoiceListing}
     \begin{hours}
          ...  % Only hour fields 
     \end{hours}
     \begin{expenses}
          ...  % Only expenses fields
     \end{expenses}
     \begin{travel}
          ...  % Only travel fields
     \end{travel}
     ...  % Accumulative data of the three groups
\end{texvoiceListing}

% Totals/averages of all entries
\begin{hours}
     ...  % Only hour fields 
\end{hours}
\begin{expenses}
     ...  % Only expenses fields
\end{expenses}
\begin{travel}
     ...  % Only travel fields
\end{travel}
...  % Accumulative data of the three groups
```
In the template you can choose any of the following keywords that will be substituted. 
Note, again, that in the outer scope averages and accumulative values are used, so the values they contain might not make very much sense to use.

- `\description`  
 The description of the entry
- `\subtotal`  
 The total price of this entry excluding VAT
- `\total`  
 The total price of this entry including VAT
- `\vatPercentage`  
 The VAT percentage on the price
- `\vat`  
 The total VAT added on the price

Each of the three sections can make use of some extra keywords. The ones marked with a `*` can also be used in the outer scope.

_Hours_
- `\duration*`  
 The amount of hours spent on this task
- `\wage*`  
 The hourly wage for this task
 
_Expenses_

_Travel_
- `\price*`  
 The price per unit of travel
- `\distance*`  
 The distance traveled
- `\from`  
 The origin of the trip
- `\to`  
 The destination of the trip
 
Throughout the entire document some other keywords related to the invoice are substituted:
- `\clientName`  
 The (company) name of the client
- `\projectID`  
 The ID given to this project
- `\invoiceID`  
 The ID of this invoice as a method of distinguishing different invoices for the same client
- `\projectDescription`  
 The description of the project
 
 ## Roadmap
 I am currently working on improving the tool quite a bit. These changes will result in the 2.0 version of texvoice, and will include the following features (checked options already implemented):
 - A proper GUI instead of the CLI interface
   - [X] Views that show the data and allow for modifications
   - [X] A list of configurable options
   - [X] Template selection
   - [ ] Template previews
   - [X] A compile button
   - [X] Display compile feedback
   - [X] Possibility to import data exports
   - [ ] Rework the CLI interface
   
 - An improved compiler
   - [X] Make the compiler more modular
   - [X] Change the data imput format
   - [X] Try to stay comliant with the compiler2
   - [X] Add maximum length for a listing
   - [X] Add listing pages
   
 - Update data loading
   - [X] Improve the loader to a new output format
   - [X] General refactoring
   
 - Update the template format
   - [X] Change the preview to an image
   - [X] Change the version file to include more data
   - [X] Add author/copyright fields
   - [X] Add a description
   - [X] Allow for custom fields
   - [X] Add required tag data to check compatibility when compiling
 
 The current tool will remain working until the work finishes on V2.0. This newer version will then replace the original tool. Check the `texvoice2` branch for the progress being made.
 
 ## Contributions
 Feel free to contribute new templates or add support for more timekeeping tools
