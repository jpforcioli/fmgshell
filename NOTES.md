# DESIGN NOTES
1. How to get something like

   ```
   set fmg ip 10.0.0.1
   set fmg username foo?
   ```

   Does it make sense?

# Naming conventions

- FMG FS: FMG file system is made of PATH or (i.e., URL), and lead to tables or
  table entries.

# TODO
1. FMGSHELL instances should use a middleware FMG instance which is in turn
   using the FMG JSON RPC API... (todo: we should remove ``FMGSHELL.api``
   attribute and only use the ``FMGSHELL.fmg`` one)   

2. Create a package 

   ```
   pip install --editable .
   ```
