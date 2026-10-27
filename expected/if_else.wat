(module
  (func $main (export "main")  (result i32) (local $x i32)
    i32.const 1
    local.set $x
    local.get $x
    if
      i32.const 7
      return
    else
      i32.const 9
      return
    end
  )
)
