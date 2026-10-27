(module
  (func $add (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.add
    return
  )
  (func $main (export "main")  (result i32)
    i32.const 2
    i32.const 5
    call $add
    return
  )
)
