# The import machinery

See [The import system](https://docs.python.org/3/reference/import.html) in 
the Python language reference.


## Meta path finders

When the named module is not found in `sys.modules` cache, Python next 
searches `sys.meta_path`, which contains a list of *meta path finder* objects.

If the *meta path finder* knows how to handle the named module, it returns a 
*spec* object. If it cannot handle the named module, it returns `None`. 
If `sys.meta_path` processing reaches the end of its list without returning a 
*spec*, then a `ModuleNotFoundError` is raised. Any other exceptions raised 
are simply propagated up, aborting the import process.

Python’s default `sys.meta_path` has three *meta path finders*: first that 
knows how to import built-in modules, second that knows how to import frozen 
modules.


### The Path Based Finder

A third default *meta path finder*, i.e. the *path based finder*, searches an 
*import path* for modules. The *import path* is a list of *path entries* that 
usually comes from `sys.path` or `package.__path__`. *Path entries* need not 
be limited to file system locations, they can refer to URLs, database queries, 
or any other location that can be specified as a string or bytes; all other 
data types are ignored.

The import machinery begins the *import path* search by calling the 
*path based finder’s* `find_spec()` method. It iterates over every entry in 
the *import path* and for each of these, looks for an appropriate 
*path entry finder* (`PathEntryFinder`) for the *path entry*.

Because this can be an expensive operation, the *path based finder* maintains 
a cache mapping *path entries* to *path entry finders*. This cache is 
maintained in `sys.path_importer_cache`.

If the *path entry* is not present in the cache, the *path based finder* 
iterates over every callable in `sys.path_hooks`. Each of the path entry hooks 
in this list is called with a single argument - the *path entry* to be 
searched. This callable may either return a *path entry finder* that can 
handle the *path entry*, or it may raise `ImportError`.


#### Path entry finders

*Path entry finders* are in a sense an implementation detail of the 
*path based finder*, and in fact, if the *path based finder* were to be 
removed from `sys.meta_path`, none of the *path entry finder* semantics would 
be invoked.

*Path entry finders* must implement the `find_spec()` method, that takes two 
arguments: the fully qualified name of the module being imported, and the 
(optional) target module. `find_spec()` returns a fully populated *spec* for 
the module.
