(module
  (memory 1)
  (data (i32.const 0) "hello")
  (data (i32.const 6) "Sriram")
  (data (i32.const 13) "Tab\there, quote: \"ok\"")
  (func $main (export "main")  (result i32) (local $greeting i32) (local $_t1 i32) (local $name i32) (local $_t2 i32) (local $msg i32) (local $_t3 i32)
    i32.const 0
    local.set $_t1
    local.get $_t1
    local.set $greeting
    i32.const 6
    local.set $_t2
    local.get $_t2
    local.set $name
    i32.const 13
    local.set $_t3
    local.get $_t3
    local.set $msg
    local.get $name
    return
  )
)
