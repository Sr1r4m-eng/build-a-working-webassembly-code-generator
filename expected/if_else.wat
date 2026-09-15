(module
  (func $main (export "main")  (result i32) (local $x i32) (local $_t1 i32) (local $_t2 i32) (local $_t3 i32) (local $_t4 i32)
    i32.const 1
    local.set $_t1
    local.get $_t1
    local.set $x
    local.get $x
    if
      i32.const 7
      local.set $_t2
      local.get $_t2
      return
    else
      i32.const 9
      local.set $_t3
      local.get $_t3
      return
    end
    i32.const 0
    local.set $_t4
    local.get $_t4
    return
  )
)
