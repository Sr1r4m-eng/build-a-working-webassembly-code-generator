(module
  (func $add (param $a i32) (param $b i32) (result i32) (local $_t1 i32)
    local.get $a
    local.get $b
    i32.add
    local.set $_t1
    local.get $_t1
    return
  )
  (func $main (export "main")  (result i32) (local $_t1 i32) (local $_t2 i32) (local $_t3 i32)
    i32.const 2
    local.set $_t1
    i32.const 5
    local.set $_t2
    local.get $_t1
    local.get $_t2
    call $add
    local.set $_t3
    local.get $_t3
    return
  )
)
