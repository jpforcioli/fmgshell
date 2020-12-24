# DESIGN NOTES
1. How to get something like

   ```
   set fmg ip 10.0.0.1
   set fmg username foo?
   ```

   Does it make sense?

# TODO
1. FMGSHELL instances should use a middleware FMG instance which is in turn
   using the FMG JSON RPC API... (todo: we should remove FMGSHELL.api and only
   use FMGSHELL.fmg)   

2. Create a package 

   ```
   pip install --editable .
   ```
3. To add a decorator in the fmgjsonrpcapi.py to create the payload, post,
   check the response and implement the debug

   Does it make sense?
   Why not just invoking a function like post_json_rpc?