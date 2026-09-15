(module
  (func $main (export "main")  (result i32) (local $x i32) (local $_t1 i32) (local $_t2 i32) (local $_t3 i32)
    i32.const 4
    local.set $_t1
    local.get $_t1
    local.set $x
    i32.const 3
    local.set $_t2
    local.get $x
    local.get $_t2
    i32.add
    local.set $_t3
    local.get $_t3
    local.set $x
    local.get $x
    return
  )
)
