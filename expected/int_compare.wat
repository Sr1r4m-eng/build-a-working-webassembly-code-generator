(module
  (func $main (export "main")  (result i32) (local $_t1 i32) (local $_t2 i32) (local $_t3 i32) (local $_t4 i32) (local $_t5 i32) (local $_t6 i32)
    i32.const 4
    local.set $_t1
    i32.const 9
    local.set $_t2
    i32.const 1
    local.set $_t3
    local.get $_t3
    if
      i32.const 1
      local.set $_t4
      local.get $_t4
      return
    else
      i32.const 0
      local.set $_t5
      local.get $_t5
      return
    end
    i32.const 0
    local.set $_t6
    local.get $_t6
    return
  )
)
