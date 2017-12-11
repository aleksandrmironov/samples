Brief
---

This approach assumes your release versioning approach approach is concatenation
of iterable int and postfix. E.g. **15-ST** means 15th staging release. 
The postfix w/o dash shoud be a jenkins job parameter(e.g. **ST**). 
The script will export new release version as a jenkins job parameter(**16-ST** in our example).

Prerequisites
---
required jenkins parameters

* Release type
* Git repository link