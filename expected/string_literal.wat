(module
  (memory 1)
  (data (i32.const 0) "hello")
  (func $main (export "main")  (result i32) (local $s i32) (local $_t1 i32)
    i32.const 0
    local.set $_t1
    local.get $_t1
    local.set $s
    local.get $s
    return
  )
)
