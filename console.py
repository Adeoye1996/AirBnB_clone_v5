#!/usr/bin/python3
"""
Command interpreter.
"""
import os
import cmd
from models import base_model, user, storage, CNC

BaseModel = base_model.BaseModel
User = user.User


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class
    """
    prompt = '(hbnb) '
    ERR = [
        '** class name missing **',
        '** class doesn\'t exist **',
        '** instance id missing **',
        '** no instance found **',
        '** attribute name missing **',
        '** value missing **',
    ]

    def preloop(self):
        """
        Handles intro to command interpreter
        """
        print('.----------------------------.')
        print('|    Welcome to hbnb CLI!    |')
        print('|   for help, input \'help\'   |')
        print('|   for quit, input \'quit\'   |')
        print('.----------------------------.')

    def postloop(self):
        """
        Handles exit to command interpreter
        """
        print('.----------------------------.')
        print('|  Well, that sure was fun!  |')
        print('.----------------------------.')

    def default(self, line):
        """
        Default response for unknown commands
        """
        pass

    def emptyline(self):
        """
        Called when an empty line is entered in response to the prompt.
        """
        pass

    def __class_err(self, arg):
        """
        Private: checks for missing class or unknown class
        """
        if len(arg) == 0:
            print(HBNBCommand.ERR[0])
            return 1
        if arg[0] not in CNC.keys():
            print(HBNBCommand.ERR[1])
            return 1
        return 0

    def __id_err(self, arg):
        """
        Private: checks for missing ID or unknown ID
        """
        if len(arg) < 2:
            print(HBNBCommand.ERR[2])
            return 1
        obj_key = f"{arg[0]}.{arg[1]}"
        if obj_key not in storage.all().keys():
            print(HBNBCommand.ERR[3])
            return 1
        return 0

    def do_airbnb(self, arg):
        """airbnb: airbnb
        SYNOPSIS: Command changes prompt string"""
        print("                      __ ___                        ")
        print("    _     _  _ _||\\ |/  \\ | _  _  _|_|_     _  _ _| ")
        print("|_||_)\\)/(_|| (_|| \\|\\__/ || )(_)| |_| )\\)/(_|| (_| ")
        print("   |                                                ")
        if HBNBCommand.prompt == '(hbnb) ':
            HBNBCommand.prompt = " /_ /_ _  /_\\n/ //_// //_/ "
        else:
            HBNBCommand.prompt = '(hbnb) '

    def do_quit(self, line):
        """quit: quit
        USAGE: Command to quit the program
        """
        return True

    def do_EOF(self, line):
        """function to handle EOF"""
        print()
        return True

    def __parse_string(self, value):
        """Parses attribute value passed as string"""
        return value.strip('"').replace('_', ' ').replace('\\"', '"')

    def __parse_number(self, value):
        """Parses attribute value passed as number"""
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def do_create(self, arg):
        """create: create [ARG]
        ARG = Class Name
        SYNOPSIS: Creates a new instance of the Class from given input ARG"""
        args = arg.split()
        if not self.__class_err(args):
            cls = CNC[args[0]]
            new_instance = cls()
            for param in args[1:]:
                key, value = param.split('=')
                if value.startswith('"') and value.endswith('"'):
                    value = self.__parse_string(value)
                else:
                    value = self.__parse_number(value)
                setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """show: show [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: Prints object of given ID from given Class"""
        args = arg.split()
        if not self.__class_err(args) and not self.__id_err(args):
            obj_key = f"{args[0]}.{args[1]}"
            print(storage.all()[obj_key])

    def do_all(self, arg):
        """all: all [ARG]
        ARG = Class
        SYNOPSIS: prints all objects of given class"""
        args = arg.split()
        if args and self.__class_err(args):
            return
        objects = storage.all(args[0] if args else None)
        print(', '.join(str(obj) for obj in objects.values()))

    def do_destroy(self, arg):
        """destroy: destroy [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: destroys object of given ID from given Class"""
        args = arg.split()
        if not self.__class_err(args) and not self.__id_err(args):
            obj_key = f"{args[0]}.{args[1]}"
            del storage.all()[obj_key]
            storage.save()

    def __check_dict(self, arg):
        """Checks if the arguments input has a dictionary"""
        if '{' in arg and '}' in arg:
            try:
                return eval(arg[arg.find('{'):])
            except (SyntaxError, ValueError):
                pass
        return None

    def __handle_update_err(self, arg):
        """Checks for all errors in update"""
        dict_arg = self.__check_dict(arg)
        args = arg.replace(',', '').replace('"', '').split()
        if not self.__class_err(args) and not self.__id_err(args):
            obj_key = f"{args[0]}.{args[1]}"
            if len(args) < 3:
                print(HBNBCommand.ERR[4])
            elif len(args) < 4 and not dict_arg:
                print(HBNBCommand.ERR[5])
            else:
                return obj_key, args, dict_arg
        return None, None, None

    def do_update(self, arg):
        """update: update [ARG] [ARG1] [ARG2] [ARG3]
        ARG = Class
        ARG1 = ID #
        ARG2 = attribute name
        ARG3 = value of new attribute
        SYNOPSIS: updates or adds a new attribute and value of given Class"""
        obj_key, args, dict_arg = self.__handle_update_err(arg)
        if obj_key:
            obj = storage.all()[obj_key]
            if dict_arg:
                for key, value in dict_arg.items():
                    setattr(obj, key, self.__parse_number(value))
            else:
                key, value = args[2], self.__parse_number(args[3])
                setattr(obj, key, value)
            obj.save()

    def __count(self, arg):
        """Counts the number of instances of a class"""
        count = sum(1 for key in storage.all().keys() if key.startswith(arg))
        print(count)

    def __parse_exec(self, cls_name, arg):
        """Parses and executes class commands"""
        cmd_map = {
            '.all': self.do_all,
            '.count': self.__count,
            '.show': self.do_show,
            '.destroy': self.do_destroy,
            '.update': self.do_update,
            '.create': self.do_create,
        }
        if '(' in arg and ')' in arg:
            cmd, args = arg.split('(')
            args = args.rstrip(')')
            cmd_func = cmd_map.get(cmd)
            if cmd_func:
                cmd_func(f"{cls_name} {args}")

    def do_BaseModel(self, arg):
        """class method with .function() syntax
        Usage: BaseModel.<command>(<id>)"""
        self.__parse_exec('BaseModel', arg)

    def do_Amenity(self, arg):
        """class method with .function() syntax
        Usage: Amenity.<command>(<id>)"""
        self.__parse_exec('Amenity', arg)

    def do_City(self, arg):
        """class method with .function() syntax
        Usage: City.<command>(<id>)"""
        self.__parse_exec('City', arg)

    def do_Place(self, arg):
        """class method with .function() syntax
        Usage: Place.<command>(<id>)"""
        self.__parse_exec('Place', arg)

    def do_Review(self, arg):
        """class method with .function() syntax
        Usage: Review.<command>(<id>)"""
        self.__parse_exec('Review', arg)

    def do_State(self, arg):
        """class method with .function() syntax
        Usage: State.<command>(<id>)"""
        self.__parse_exec('State', arg)

    def do_User(self, arg):
        """class method with .function() syntax
        Usage: User.<command>(<id>)"""
        self.__parse_exec('User', arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
