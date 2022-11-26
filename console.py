#!/usr/bin/python3
"""This is the console module that can be used as command interpreter
interactively and non interactively"""
import cmd
import sys
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review
from models.__init__ import storage


class HBNBCommand(cmd.Cmd):
    """This is the console class"""
    intro = 'Welcome to the HBNB console.Type help or ?\n'
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {'BaseModel': BaseModel, 'State': State,
               'City': City, 'Place': Place, 'Amenity': Amenity,
               'User': User, 'Review': Review}

    d_commands = ['all', 'create', 'show', 'destroy', 'update']

    data_type = {'number_rooms': int, 'price_by_night': int,
                 'longitude': float, 'latitude': float,
                 'number_bathrooms': int, 'max_guest': int}

    def preloop(self):
        """If an attribute isatty is printed"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def precmd(self, line):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements
        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line
        try:  # parse line left to right
            pline = line[:]  # parsed line
            # isolate <class name>
            _cls = pline[:pline.find('.')]
            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception
            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple
                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced
                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                             and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception as mess:
            pass
        finally:
            return line

    def do_quit(self, args):
        """Stop recording the window and quit: QUIT"""
        print("Thank you for using the HBNB console")
        exit()

    def help_quit(self):
        """Help on quit"""
        print('Quits with formatting\n')

    def emptyline(self):
        """Skips emptylines"""
        pass

    def help_emptyline(self):
        """Help on emptyline"""
        print('Ignores empty lines\n')

    def do_EOF(self):
        """Shows the end of the file"""
        print()
        exit()

    def help_EOF(self):
        """help for EOF"""
        print('Shows the end of file or line\n')

    def do_create(self, args):
        """Creates a new instance of the object"""
        class_name = args
        if not args:
            print("** class name missing **")
        elif class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")

        new_instance = HBNBCommand.classes[args]()

        storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        """Help on create"""
        print('Creates a new instance of BaseModel')
        print('saves instance to the JSON file and prints the id\n')

    def do_show(self, args):
        """Shows the string representation of the instances"""
        new = args.partition(" ")
        class_name = new[0]
        class_id = new[2]
        # guard against trailing args
        if class_id and ' ' in class_id:
            class_id = class_id.partition(' ')[0]
        if not class_name:
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not class_id:
            print("** instance id missing **")
            return
        key = class_name + "." + class_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help on end of file"""
        print('Prints the string representation of an instance\n')

    def do_destroy(self, args):
        """Deletes instances of a certain class"""
        new = args.partition(" ")
        class_name = new[0]
        class_id = new[2]
        if class_id and ' ' in class_id:
            class_id = class_id.partition(' ')[0]
        if not class_name:
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not class_id:
            print("** instance id missing **")
            return
        key = class_name + "." + class_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help on destroy"""
        print('Deletes an instance of the class')
        print('Saves the changes to the JSON file\n')

    def do_all(self, args):
        """prints a string representation of all instances"""
        l_list = []
        if args:
            args = args.split(' ')[0]  # remove trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    l_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                l_list.append(str(v))
        print(l_list)

    def help_all(self):
        """Help on all"""
        print('Prints all string representation of all instances\n')

    def do_update(self, args):
        """Updates instances accordingly"""
        class_name = class_id = att_name = att_val = kwargs = ''
        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            class_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        args = args[2].partition(" ")
        if args[0]:
            class_id = args[0]
        else:
            print("** instance id missing **")
            return

        key = class_name + "." + class_id
        if key not in storage.all():
            print("** no instance found **")
            return
        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]
            args = args.partition(' ')
            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]
            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]
            args = [att_name, att_val]
        # retrieve dictionary of current objects
        new_dict = storage.all()[key]
        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)
                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})
        new_dict.save()  # save updates to file

    def help_update(self):
        """Help on update"""
        print('Updates an instance by adding or updating attribute')
        print("Usage: update <className> <id> <attName> <attVal>")
        print('Saves changes into the JSON file\n')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
