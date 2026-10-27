(module
  (func $main (export "main")  (result i32) (local $x i32) (local $_t1 i32) (local $_t2 i32) (local $_t3 i32) (local $_t4 i32) (local $_t5 i32) (local $_t6 i32) (local $_t7 i32) (local $_t8 i32) (local $_t9 i32)
    i32.const 0
    local.set $_t1
    local.get $_t1
    local.set $x
    block
      loop
        i32.const 3
        local.set $_t2
        local.get $x
        local.get $_t2
        i32.lt_s
        local.set $_t3
        local.get $_t3
        i32.eqz
        br_if 1
        i32.const 1
        local.set $_t4
        local.get $x
        local.get $_t4
        i32.eq
        local.set $_t5
        local.get $_t5
        if
          i32.const 1
          local.set $_t6
          local.get $x
          local.get $_t6
          i32.add
          local.set $_t7
          local.get $_t7
          local.set $x
        else
          i32.const 1
          local.set $_t8
          local.get $x
          local.get $_t8
          i32.add
          local.set $_t9
          local.get $_t9
          local.set $x
        end
        br 0
      end
    end
    local.get $x
    return
  )
)
