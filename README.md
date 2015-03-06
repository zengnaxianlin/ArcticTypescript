ArcticTypescript
================

 * TypeScript language auto completion
 * TypeScript language syntax highlighting
 * TypeScript language error highlighting
 * A build System
 * Fast access to errors via shortcuts and clicks
 * Goto definition
 * View type



Commands and Shortcuts
----------------------------------------------------------------------------

 * `ctrl + space`           trigger code completion.
 * `alt + shift + e e`      error view
 * `alt + shift + e h`      jump to 1st error
 * `alt + shift + e j`      jump to 2nd error
 * `alt + shift + e k`      jump to 3rd error
 * `alt + shift + e l`      jump to 4th error
 * `F1`                     show details about type under cursor
 * `F4`                     jump to definition
 * `F5`                     reload (to this if autocompletion is missing something)
 * `F8` or `ctrl + b`       Build the project.



Settings
----------------------------------------------------------------------------


You need to configure typescript using a `tsconfig.json` file. Place this
file in your project folder or at least in some parent folder of your source
files.

Minimal Example `tsconfig.json`:

    {
        "compilerOptions": {
            "out": "out.js",
            "sourceMap": true,
            "target": "es5"
        },
        "files": [
            "main.ts"
        ],
    }

More `compilerOptions`:
 * `target`              (string) 'es3'|'es5' (default) | 'es6'
 * `module`              (string) 'amd'|'commonjs' (default)
 * `declaration`         (boolean) Generates corresponding `.d.ts` file
 * `out`                 (filepath) Concatenate and emit a single file
 * `outDir`              (folderpath) Redirect output structure to this directory
 * `noImplicitAny`       (boolean) Error on inferred `any` type
 * `removeComments`      (boolean) Do not emit comments in output
 * `sourceMap`           (boolean) Generates SourceMaps (.map files)
 * `removeComments`      (boolean)  Do not emit comments to output.
 * `sourceRoot`          (folder) Optionally specifies the location where debugger
                         should locate TypeScript source files after deployment
 * `mapRoot`             (folder) Optionally Specifies the location where debugger
                         should locate map files after deployment
 * `preserveConstEnums`  (boolean) Do not erase const enum
                         declarations in generated code.
 * `suppressImplicitAnyIndexErrors` (boolean) Suppress noImplicitAny errors for
                        indexing objects lacking index signatures.

All pathes are relative to `tsconfig.json`. These are exactly the options for
the typescript compiler: Refer to `tsc --help`.



`"files" : []` : Define the files which should be compiled. **At least 1 file is
                 required.** You only need to specify the file from the top / root
                 of your internal reference tree (your main.ts). But it does no
                 harm to specify more files.


### ArcticTypescript settings


You can configure ArcticTypescript as well (type, default):

 * `activate_build_system`     (boolean, true)
 * `auto_complete`             (boolean, true)
 * `node_path`                 (string, null) If null, then nodejs must be in $PATH
 * `tsc_path`                  (string, null) If null, it will search a
                                              `node_modules` dir with `tsc` or
                                              use ArcticTypescript's `tsc`
 * `error_on_save_only`        (boolean, false)
 * `build_on_save`             (boolean, false)
 * `show_build_file`           (boolean, false) show the compiled output after build
 * `pre_processing_commands`   ([string], [])
 * `post_processing_commands`  ([string], [])


Where to store these settings:

 * For personal settings across all typescript projects:
    - `<sublime config dir>/Packages/User/Preferences.sublime-settings ['ArcticTypescript'][KEY]`
      GUI: Menu -> Preferences -> "Settings - User"
    - `<sublime config dir>/Packages/User/ArcticTypescript.sublime-settings [KEY]`
        - GUI Menu -> Preferences -> Package Settings ->
          ArcticTypescript -> "Settings - User"
 * For personal, project specific settings
    - `<ProjectSettings>.sublime-settings ['settings']['ArcticTypescript'][KEY]`
        - GUI: Menu -> Project -> "Edit Project"
 * If you are not part of a team or for settings for everyone or for project
   specific settings if you don't have created a sublime project
    - tsconfig.json['ArcticTypescript'][KEY]




Installation
----------------------------------------------------------------------------



### Features


### Commands:

Create a project file first (read below).



### Dependencies
- node.js
- tsc for the build system that you install via <code>npm install -g typescript</code> (http://www.typescriptlang.org/)


### OS
Tested on Ubuntu so far. For Windows & OSX please submit any issues.


### Installation

- Install Package Control for Sublime Text 3: https://sublime.wbond.net/installation
- Sublime command: <code>Package Control: Install Package</code> > <code>ArcticTypescript</code>

## Your Project

##### General Information about projects and ArcticTypescript

This plugin uses the typescript-tools (https://github.com/clausreinke/typescript-tools) to provide code completion, parsing, ...

To init the services, a so-called root file is required. This enables the tools to find all typescript files which belong together. Currently this is not implemented properly. Until this is fixed, i recommend to ONLY use ONE root file.

If you have multiple entry points, use the one which includes more references. For example use test.ts instead of main.ts as rootfile, so all test files will be included in the internal project tree of the typescript tools. Or create a kind of fake root.ts file that references all your other entry points (main.ts, test.ts, ...).

##### Project Settings

For ArcticTypescript to work, you must define some settings either

1. inside your <code>project_name.sublime-project</code> file if you have one
2. or by creating a <code>.sublimets</code> at the root of your project folder.

You can look inside the <code>example folder</code> for setup examples.

Temporarily, you need to define the compiler settings twice:

You will also need a <code>tsconfig.json</code> file.

Example:

	{
		"compilerOptions" : {
			"target" : "es5",
			"module" : "commonjs"
		}
	}

Refer to https://www.npmjs.com/package/tsconfig for more options.

Autocompletion and error view will now be initialized using <code>tsconfig.json</code>. The integrated build system still uses the <i>old</i> compiler options inside of <code>.sublimets</code> or <code>project_name.sublime-project</code>. <b>In future, all compiler options will move to tsconfig.json</b>

If you open any .ts file and ArcticTypescript can't find any project settings, you will be promted to create them.

To open a project, you need to open the folder where your project is with <code>File > Open Folder ...</code> or <code>Project > Open Project ...</code>

**Watch out, the settings (names, ..) may change in future versions of ArcticTypescript. If you encounter problems, read the changelog and readme first.**

##### Project Settings in a projectname.sublime-project file

	"settings":
	{
			"typescript":
			{
				"roots":[
					"path/from/top/folder/to/your/root/file_1.ts"
				]
			}
	}

And also add (optional) project settings :

	"settings":
	{
		"typescript":
		{
			"roots":[
				"path/from/top/folder/to/your/root/file_1.ts",
			],
			"settings":{
				"auto_complete":true,
				"node_path":"none",
				"error_on_save_only":false,
				"build_on_save":false,
				"show_build_file":false,
				"build_parameters":{
					"pre_processing_commands":[],
					"post_processing_commands":[],
					"output_dir_path":"none",
					"concatenate_and_emit_output_file_path":"none",
					"source_files_root_path":"none",
					"map_files_root_path":"none",
					"module_kind":"none",
					"allow_bool_synonym":false,
					"allow_import_module_synonym":false,
					"generate_declaration":false,
					"no_implicit_any_warning":false,
					"skip_resolution_and_preprocessing":false,
					"remove_comments_from_output":false,
					"generate_source_map":false,
					"ecmascript_target":"ES3"
				}
			}
		}
	}

The build parameters (except for pre_processing_commands and post_processing_commands) are converted into the command line options of the typescript compiler tsc.

- Either <code>output_dir_path</code> (for --outDir) or <code>concatenate_and_emit_output_file_path</code> (for --out) must contain a file path/directory. If you want to insert a relative path, it has to start with a dot: <code>.</code> The relative path is relative to the folder of the root file.
- For any path related config option: If no path is given, please insert <code>"none"</code>.
- <code>show_build_file</code> displays the compiled file in an extra view inside of sublime.

##### Project Settings in a .sublimets file

You want to create a **single root file project** and don't want to create a sublime-project
You can create a <code>.sublimets</code> file in the folder containing the typescript root file :

	{
			"root":"root_file_name.ts"
	}

And also add (optional) your project settings :

	{
		"root":"root_file_name.ts",
		"settings":{
			"auto_complete":true,
			"node_path":"none",
			"error_on_save_only":false,
			"build_on_save":false,
			"show_build_file":false,
			"build_parameters":{
				"pre_processing_commands":[],
				"post_processing_commands":[],
				"output_dir_path":"none",
				"concatenate_and_emit_output_file_path":"none",
				"source_files_root_path":"none",
				"map_files_root_path":"none",
				"module_kind":"none",
				"allow_bool_synonym":false,
				"allow_import_module_synonym":false,
				"generate_declaration":false,
				"no_implicit_any_warning":false,
				"skip_resolution_and_preprocessing":false,
				"remove_comments_from_output":false,
				"generate_source_map":false,
				"ecmascript_target":"ES3"
			}
		}
	}


### Settings:
You can acces the plugin settings from <code>Preferences > Packages Settings > ArcticTypescript</code>, to modify the settings please copy the default settings inside the user settings one, and make your modification there otherwise your settings will be override by an update of the plugin, or put the settings inside your project file.


You have 6 settings available:

1. <code>auto_complete</code>: if you want to have sublime normal completion with typescript completion
2. <code>node_path</code>: to set you node path
3. <code>error_on_save_only</code>: to highlight errors only while saving or while typing, the default is showing error highlighting while typing
4. <code>build_on_save</code>: to build the project each time you save
5. <code>show_build_file</code>: to show the resulting javascript file of the current TypeScript file in a split view when building
6. the build parameters


		{
			"auto_complete":true,
			"node_path":"none",
			"error_on_save_only":false,
			"build_on_save":false,
			"show_build_file":false,
			"build_parameters":{
				"pre_processing_commands":[],
				"post_processing_commands":[],
				"output_dir_path":"none",
				"concatenate_and_emit_output_file_path":"none",
				"source_files_root_path":"none",
				"map_files_root_path":"none",
				"module_kind":"none",
				"allow_bool_synonym":false,
				"allow_import_module_synonym":false,
				"generate_declaration":false,
				"no_implicit_any_warning":false,
				"skip_resolution_and_preprocessing":false,
				"remove_comments_from_output":false,
				"generate_source_map":false,
				"ecmascript_target":"ES3"
			}
		}

##### auto_complete:
you can have normal sublime auto completion with typescript completion (if changed you need to restart sublime)

		"auto_complete":true|false


##### node_path:
You can set the path to node : (if changed you need to restart sublime)

		"node_path":"/your/path/to"


##### error_on_save_only:
Error highlighting while typing (will lag a bit du to calculation and this cannot be changed):


		"error_on_save_only":false


Error highlighting only shown when saving:


		"error_on_save_only":true


##### build_on_save:
On save the file can be automaticaly built or not :

		"build_on_save":true|false


##### show_build_file:
You can show the resulting javascript file of the current TypeScript file in a split view when building :

		"show_build_file":true|false


##### build_parameters:
I've added a build system that take most of the command line parameters of TSC, i'll not explain them here, you can install TSC and look at the parameters via <code>tsc -h</code>

And you also have two extra parameters that are <code>pre_processing_commands</code> and <code>post_processing_commands</code> that give you the opportunity to do command line things before and after <code>tsc</code> compiling

These are the default values:


		"build_parameters":{
			"pre_processing_commands":[],
			"post_processing_commands":[],
			"output_dir_path":"none",
			"concatenate_and_emit_output_file_path":"none",
			"source_files_root_path":"none",
			"map_files_root_path":"none",
			"module_kind":"none",
			"allow_bool_synonym":false,
			"allow_import_module_synonym":false,
			"generate_declaration":false,
			"no_implicit_any_warning":false,
			"skip_resolution_and_preprocessing":false,
			"remove_comments_from_output":false,
			"generate_source_map":false,
			"ecmascript_target":"ES3"
		}

Here's an example that do:

1. One pre processing command : <code>node .settings/.components</code>
2. The actual compilation with an output dir and amd module : <code>tsc /absolute/path/to/filename.ts --outDir ./.build --module amd</code>
3. Two post processing commands : <code>node .settings/.silns.js</code> and <code>r.js.cmd -o .settings/.build.js</code>

		"build_parameters":{
			"pre_processing_commands":[
				"node .settings/.components"
			],
			"post_processing_commands":[
				"node .settings/.silns.js",
				"r.js.cmd -o .settings/.build.js"
			],
			"output_dir_path":"./.build",
			"concatenate_and_emit_output_file_path":"none",
			"source_files_root_path":"none",
			"map_files_root_path":"none",
			"module_kind":"amd",
			"allow_bool_synonym":false,
			"allow_import_module_synonym":false,
			"generate_declaration":false,
			"no_implicit_any_warning":false,
			"skip_resolution_and_preprocessing":false,
			"remove_comments_from_output":false,
			"generate_source_map":false,
			"ecmascript_target":"ES3"
		}


### Usage:

##### Initialisation:
When you load a .ts file the plugin will initialize the root file or the current file and it can take some time for huge project.

The Sublime Text Status bar will indicate Typescript initializing during this phase and disapear when it's finished

##### Show Type:
you can click on variable or a method and press <code>F1</code> to have detail about it (doc comments etc...)

##### Got to definition:
you can click on variable or a method and press <code>F4</code> to go to the definition

##### Outline View:
you can open an <code>Outline view</code> by pressing <code>F3</code> on a file to list class variables and methods tou can then click on an item to scroll towards it

##### Auto-completion:
You can circle through the function variables (if there's some) like with the snippets with the <code>tab</code> key

##### Error highlighting:
You can click on highlighted part to see the error description in the status bar

##### Error View:
You have the possibility to open an <code>Error view</code> that will list all the errors accross all your project file with the command <code>alt+shift+e</code>
You can then click on each row, it'll open or focus the already open file concerned by the error.

##### Reloading the project:
You have the possibility to <code>reload</code> the project by pressing <code>F5</code>, you can see in the console when the reload is finished

##### Building the project:
you can build the current project with <code>F8</code> on a file. if you have activated <code>show_build_file</code> option it will show a <code>Split view</code> with the corresponding javascript file



Credits
----------------------------------------------------------------------------

TypeScript plugin for Sublime Text 3 using TypeScript tools : https://github.com/clausreinke/typescript-tools

I'm using the same error icons has SublimeLinter.
I took inspiration from: https://github.com/raph-amiard/sublime-typescript





Notes for Upgraders / People which used T3S before
----------------------------------------------------------------------------

This is a clone of the Typescript T3S Plugin, but with a lots of changes. If you switch to ArcticTypescript, please:
 - read this readme
 - uninstall T3S
 - only use one root file
 - delete the *.sublime-workspace files in your projects
 - close all file tabs in your old T3S Projects
 - update your key binding overrides, The new key is 'ArcticTypescript'





Compatibility
----------------------------------------------------------------------------

Sublime Text 2 is not supported anymore: Use the T3S plugin instead of this
one for Sublime Text 2 users.




Important Changes
----------------------------------------------------------------------------


v0.5.0:
*  You will need a new config file called tsconfig.json
*  Updated to TS 1.5 via typescript-tools (switching to tsserver will come soon)
*  Dropped support for Outline view, since typescript-tools has dropped support
   for this. This feature will come back again with tsserver.

v0.4.0:
*  build system: (relative) paths with spaces are now enclosed in "" automatically
*  > If you used additional "" to workaround the issue, you have to remove them,
   refer to messages/0.4.0.txt

v0.3.0:
*  relative root files now have a different base directory
*  The default shortcut to switch to the error view changed to: CTRL + ALT + E
*  There are 4 new shortcuts to jump to the first four Errors:
   CTRL + ALT + E + H (or J, K, L)
