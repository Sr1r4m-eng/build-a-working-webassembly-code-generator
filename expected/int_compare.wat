(module
  (func $main (export "main")  (result i32)
    i32.const 1
    if
      i32.const 1
      return
    else
      i32.const 0
      return
    end
  )
)
