(module
  (func $main (export "main")  (result i32) (local $x i32)
    i32.const 0
    local.set $x
    block
      loop
        local.get $x
        i32.const 3
        i32.lt_s
        i32.eqz
        br_if 1
        local.get $x
        i32.const 1
        i32.add
        local.set $x
        br 0
      end
    end
    local.get $x
    return
  )
)
