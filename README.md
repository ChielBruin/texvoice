# texvoice
Texvoice allows you to simply generate invoices using latex templates. This way you can fully customize the invoice to your needs. Texvoice does not only support the amount of hours spent on a task, but also travel costs and general expenses. The tool also allows you to import data directly from exports of certain timekeeping applications, but is also very flexible as you can also create/review/change the data yourself before generating the invoice. Texvoice is primarily focussed on its GUI, but a commandline interface is also present.  
Texvoice comes pre-packaged with a number of templates, but creating your own is encouraged in order to create a fully personalized invoice that fits your needs.

## Requirements
Texvoice is verified to run on Linux, but it might be possible that calling the Latex compiler also works on Windows and Mac.
- Python 3
- Latex

## Template structure
The templates used by texvoice describe how an invoice should be created. This is done using a Latex file with additional environments that mark locations where data should be inserted.  
A template file is a `.zip` archive containing all the files that are needed by the template file itself and some additional files. This gives a template with the following file structure:
```
MyTemplate.zip
     |
     | properties.json
     | example.png
     | template.tex
     | include/
```
Here `template.tex` is the latex file containing the actual template and the optional include folder contains all the files that the Latex compiler needs to create the document. Next `example.png` is a thumbnail of the end result with a size of 200x300 pixels (WxH). Lastly the properties file contains all the information about the template. This ranges from a description and a license to the required Latex packages to compile and a list of custom static macros.

### Environments
The template latex file as based around a number of environments and macros. These are replaced by texvoice in order to create the final Latex source file that is converted to a PDF. The macros can be used in two cases, either globally or locally for a single data entry. These two types are distinguished by the current environment. The `texvoiceListing` environment is an environment that is duplicated for each entry in the dataset and contains all the local macros. Multiple instances of such an environment can be created, where data that did not fit will overflow to the next instance. For this to work correctly, a maximum number of repititions can be given to limit the size of a single instance. In addition to using multiple instances, one could also wrap it inside a `texvoicePage` environment that allows to create multiple instances of the `texvoiceListing` using only a single delaration. This environment accepts an optional argument that will be prefixed beginning from the secon application. Using for example `\clearpage` here, allows you to create as many new pages as are possible to fit all the data.

Within both the global and local scopes, there exist four distinct groups. The first three are wrapped in their own environments (`hours`, `expenses`, `travel`) and contain the actual data replacement macros and the last acts as an accumulation of the three groups containing, among others, totals of the prices. When used in local scope the macros will only apply to a single data entry and when used globally only the totals will be presented. In this case you must note that for some fields an average is computed, making usage of these fields not very usefull in some cases.

Below the layout of all the environments is made more graphical.
``` Latex
% Repeat this untill no more data can be applied
\begin{texvoicePage}[\clearpage]        % Allows for an optional prefix
    % Listing for each data entry
    \begin{texvoiceListing}[9]          % Optional maximum size of the listing
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
\end{texvoicePage}

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
### Macros
In the environment structure described in the section above, numerous macros can be used. Some macros work in every environment, while others only work in some. Not all macros are available in the global scope, but the supported ones are marked with a *. Note, again, that in the outer scope averages and accumulative values are used, so the values they contain might not make very much sense to use in your case.

At each point you can use the following macros:  
- `\subtotal`  
 The total price excluding VAT
- `\total`  
 The total price including VAT
- `\vatPercentage`  
 The VAT percentage on the price
- `\vat`  
 The total VAT added to the price

For each of the three other environments, you can use the following macros:  
_Hours_
- `\description`  
 The description of the task
- `\duration*`  
 The amount of hours spent on this task
- `\wage*`  
 The hourly wage for this task
 
_Expenses_
- `\description`  
 The description of the bought object
- `\price`*  
 The price of the object bought

_Travel_
- `\distance*`  
 The distance traveled
- `\price`*  
 The price per distance unit
- `\from`  
 The origin of the trip
- `\to`  
 The destination of the trip
 
In addition to the macros described here, a template is also free to define more macros with static values. These can be useful for an invoice ID, or the name of a client.

## Data format
Texvoice uses an intermediate data format to pass data from the loader to the GUI and to the compiler. When using the CLI interface, you will need to work with this format. Due to the modular nature of the compiler, this allows you to introduce your own environments and use it for other things than invoices. 

## CSV config files

## Supported imput methods
Data can in theory be loaded from various formats, but in practice only supports a few. Texvoice currently has support for CSV files in combination with CSV-configs describing which data is stored in which column. Besides this mapping the configs also allow for some simple function for correctly formatting the data. For the following timekeeping tools a config is available, such that they can be used to import data from:  
- [Timesheet](https://play.google.com/store/apps/details?id=com.rauscha.apps.timesheet) [Dutch version]

Currently only the Dutch version is supported, due to a language specific `.csv`. format.

## Development
Currently texvoice is on its version 2. Previously the tool was mostly a proof of concept with a terrible commandline interface for running it. For version 2, almost the entire codebase was rewritten to make the compiler way more modular (see (dataFormat)[the data format section]), introduce a GUI, update the template format and make it more reliable as a whole.  

At this point there are still a number of known issues with the program, but as the tool already works way better than the original program it was decided to move to the newer version. All the needed functionalities are there, but some things need some attention to the details to make them perfect. For an overview of known issues, see the issues that are currently open.  

Feel free to fix issues, add new functionalities or create more templates.
