# reclusive_database

Little database.   
Console input\output.  
Uses only RAM.  
One line - one action.  
Python 2.7.  

Commands:
* ```SET``` - save arg variable with some value.
* ```GET``` - return arg variable's value or None.
* ```UNSET``` - delete arg variable.
* ```COUNTS``` - count arg values.
* ```FIND``` - find all variables with arg value.
* ```END``` - stop program (or simply hit Enter 2 times in a row).

Also, database supports transactions.

* ```BEGIN``` - begin transaction.
* ```ROLLBACK``` - rollback last transaction.
* ```COMMIT``` - apply all transactions changes.

Just print ```python pydb.py``` for start or ```python pydb.py -t``` for start with test mode.  

Good luck.
