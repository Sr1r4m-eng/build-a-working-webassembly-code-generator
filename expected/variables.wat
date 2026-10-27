(module
  (func $main (export "main")  (result i32) (local $x i32)
    i32.const 4
    local.set $x
    local.get $x
    i32.const 3
    i32.add
    local.set $x
    local.get $x
    return
  )
)
