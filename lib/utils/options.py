

# the values are validators!

compileroptions_validations = {
	"target" : ["es3", "es5", "es6"], #?: string;            // 'es3'|'es5' (default) | 'es6'
    "module" : ["amd", "commonjs"], #?: string;            // 'amd'|'commonjs' (default)
    "declaration" : bool, #?: boolean;      // Generates corresponding `.d.ts` file
    "out" : "(.*[^/]\.js)$", #?: string;               // Concatenate and emit a single file
    "outDir" : "(.+/)$", #?: string;            // Redirect output structure to this directory
    "noImplicitAny" : bool, #?: boolean;    // Error on inferred `any` type
    "suppressImplicitAnyIndexErrors" : bool,
    "removeComments" : bool, #?: boolean;   // Do not emit comments in output
    "sourceMap" : bool, #?: boolean;        // Generates SourceMaps (.map files)
    "sourceRoot" : str, #?: string;        // Optionally specifies the location where debugger should locate TypeScript source files after deployment
    "mapRoot" : str, #?: string; 			 // Optionally Specifies the location where debugger should locate map files after deployment
    "preserveConstEnums" : bool, #?:boolean;	// Do not erase const enum declarations in generated code.
    "removeComments" : bool, #?: boolean;  //  Do not emit comments to output.
}
allowed_compileroptions = list(compileroptions_validations.keys())


settings_validations = {
	"activate_build_system": bool,     #?:boolean;   default: true
	"auto_complete": bool,             #?:boolean,   default: true
	"node_path": bool,                 #?:string,    default: null -> nodejs in $PATH
	"tsc_path": bool,                  #?:string,    default: null -> search a node_modules dir with tsc or use ArcticTypescript's tsc
	"error_on_save_only": bool,        #?:boolean,   default: false
	"build_on_save": bool,             #?:boolean,   default: false
	"show_build_file": bool,           #?:boolean,   default: false
	"pre_processing_commands": list,   #?:[string]   default: []
	"post_processing_commands": list,  #?:[string]   default: []
}
allowed_settings = list(settings_validations.keys())