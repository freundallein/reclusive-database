# -*- coding: utf-8 -*-
import sys


class Database:
    """Class for Database or Transaction. CRUD."""

    def __init__(self):
        """Create database - simple dict."""
        self.base = {}

    def set(self, var, value):
        """Set database pair {var: value}."""
        self.base[var] = value

    def unset(self, var):
        """Delete database key."""
        if self.base.get(var) is not None:
            del self.base[var]

    def trans_unset(self, var):
        """Set database variable to None for updating db while transactions committed."""
        self.base[var] = None

    def get(self, var):
        """Return database value."""
        return self.base.get(var)

    def counts(self, value):
        """Count all variables with arg value and return integer."""
        return len(self.find(value))

    def find(self, value):
        """Find all variables with arg value and return dict."""
        items = self.base.items()
        result = {k: v for k, v in items if v == value}
        return result

    def update(self, db):
        """Update database with transaction (arg db)."""
        self.base.update(db.base)

    def __str__(self):
        return str(self.base)


class DatabaseManager:
    """Manager for main database and transactions. Adds every transaction to queue on creation."""
    queue = []

    def __init__(self):
        """Set working flag and init main database."""
        self.working = True
        main_db = Database()
        self.add(main_db)

    def get_working(self):
        """Return working flag."""
        return self.working

    def start_transaction(self):
        """Init new transaction creation."""
        transaction = Database()
        self.add(transaction)

    def end(self):
        """Stop program."""
        self.working = False

    def add(self, db):
        """Add database or transaction to queue."""
        self.queue.append(db)

    def get_last_transaction(self):
        """Return last transaction id."""
        last_id = len(self.queue) - 1
        if last_id >= 0:
            return self.queue[last_id]
        else:
            print 'Error.'

    def get_item(self, var):
        """Return database variable (last fixed in any transaction or main db)."""
        val = None
        for item in reversed(self.queue):
            val = item.get(var)
            if val:
                break
        return val

    def set_item(self, var, value):
        """Set database pair {var: value}."""
        current = self.get_last_transaction()
        current.set(var, value)

    def unset_item(self, var):
        """Unset variable in main database or transaction (if exists)."""
        current = self.get_last_transaction()
        if len(self.queue) > 1:
            current.trans_unset(var)
        else:
            current.unset(var)

    def find_vars(self, value):
        """Find all variables with arg value. Prevent reading recurrent data. Return list."""

        def _check_for_cross(result_dict, current_db):
            """Delete result record if variable was unset or set in different transactions."""
            checked_dict = result_dict.copy()
            for key in checked_dict:
                if checked_dict.get(key) != current_db.get(key) and current_db.get(key, '#') is not '#':
                    del result_dict[key]

        accumulation = {}
        for item in self.queue:
            var = item.find(value)
            if var is not None:
                accumulation.update(var)
            _check_for_cross(accumulation, item)
        if len(accumulation) < 1:
            return None
        return accumulation.keys()

    def count_values(self, value):
        """Count all variables with arg value and return integer."""
        if self.find_vars(value) is not None:
            return len(self.find_vars(value))
        else:
            return 0

    def rollback(self):
        """Transaction rollback."""
        if len(self.queue) > 1:
            self.queue.pop(len(q.queue) - 1)
        else:
            print 'There is no transaction for rollback.'

    def clean(self, db):
        """Cleaning main database from {key: None} pairs."""
        db_items = db.base.copy().items()
        for k, v in db_items:
            if v is None:
                del db.base[k]

    def commit(self):
        """Commit ALL transactions, then clean main database."""
        while len(self.queue) > 1:
            last_id = len(self.queue) - 1
            prev = self.queue[last_id - 1]
            curr = self.queue.pop(last_id)
            prev.update(curr)
        self.clean(self.queue[0])

    def help(self):
        """Help message printing."""
        msg = '''
        How to use:                             For transactions use:
        SET    variable value(int or string)    BEGIN
        UNSET  variable                         ROLLBACK
        GET    variable                         COMMIT
        FIND   value
        COUNTS value
        END
        '''
        print msg

    def __str__(self):
        return str(self.queue)


def parse_input(line):
    """Parse input line for commands and args. Return dict."""
    comm = {}
    sep = line.split(' ')
    comm['action'] = sep[0]
    if len(sep) > 1:
        comm['arg1'] = sep[1]
        if len(sep) > 2:
            comm['arg2'] = sep[2]
        else:
            comm['arg2'] = ''
    else:
        comm['arg1'] = ''
    return comm


def process_command(comm):
    """Process dict with commands. Call for DatabaseManager Object functions."""
    command = comm.get('action').upper()
    arg1 = comm.get('arg1')
    arg2 = comm.get('arg2')
    if command == 'SET' and arg1.isalpha() and arg2.isalnum():
        q.set_item(arg1, arg2)
    elif command == 'UNSET' and arg1.isalpha():
        q.unset_item(arg1)
    elif command == 'GET' and arg1.isalpha():
        print q.get_item(arg1)
    elif command == 'COUNTS' and arg1.isalnum():
        print q.count_values(arg1)
    elif command == 'FIND' and arg1.isalnum():
        print q.find_vars(arg1)
    elif command == 'END' or command == '':
        q.end()
    elif command == 'BEGIN':
        q.start_transaction()
    elif command == 'ROLLBACK':
        q.rollback()
    elif command == 'COMMIT':
        q.commit()
    elif command == 'HELP':
        q.help()
    elif command == 'R' and test_mode():
        print 'Manager queue - ', q
        for item in q.queue:
            print id(item), item
    else:
        print 'Unknown command. Type HELP for help.'


def test_mode():
    """If start app in console with '-t' key return True for entering testmode."""
    try:
        if sys.argv[1] == '-t':
            return True
    except IndexError:
        return False


if __name__ == '__main__':
    q = DatabaseManager()
    q.help()
    while q.get_working():
        input_line = raw_input()
        command_line = parse_input(input_line)
        process_command(command_line)
