(module
  (func $abs_value (param $n i32) (result i32)
    local.get $n
    i32.const 0
    i32.lt_s
    if
      i32.const 0
      local.get $n
      i32.sub
      return
    else
      local.get $n
      return
    end
  )
  (func $max_value (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.gt_s
    if
      local.get $a
      return
    else
      local.get $b
      return
    end
  )
  (func $min_value (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.lt_s
    if
      local.get $a
      return
    else
      local.get $b
      return
    end
  )
  (func $factorial (param $n i32) (result i32)
    local.get $n
    i32.const 1
    i32.le_s
    if
      i32.const 1
      return
    else
      local.get $n
      local.get $n
      i32.const 1
      i32.sub
      call $factorial
      i32.mul
      return
    end
  )
  (func $fibonacci (param $n i32) (result i32) (local $_t5 i32)
    local.get $n
    i32.const 1
    i32.le_s
    if
      local.get $n
      return
    else
      local.get $n
      i32.const 1
      i32.sub
      call $fibonacci
      local.set $_t5
      local.get $_t5
      local.get $n
      i32.const 2
      i32.sub
      call $fibonacci
      i32.add
      return
    end
  )
  (func $gcd (param $a i32) (param $b i32) (result i32) (local $remainder i32)
    block
      loop
        local.get $b
        i32.const 0
        i32.ne
        i32.eqz
        br_if 1
        local.get $a
        local.get $a
        local.get $b
        i32.div_s
        local.get $b
        i32.mul
        i32.sub
        local.set $remainder
        local.get $b
        local.set $a
        local.get $remainder
        local.set $b
        br 0
      end
    end
    local.get $a
    return
  )
  (func $sum_range (param $n i32) (result i32) (local $total i32) (local $i i32)
    i32.const 0
    local.set $total
    i32.const 1
    local.set $i
    block
      loop
        local.get $i
        local.get $n
        i32.le_s
        i32.eqz
        br_if 1
        local.get $total
        local.get $i
        i32.add
        local.set $total
        local.get $i
        i32.const 1
        i32.add
        local.set $i
        br 0
      end
    end
    local.get $total
    return
  )
  (func $is_even (param $n i32) (result i32)
    local.get $n
    i32.const 2
    i32.div_s
    i32.const 2
    i32.mul
    local.get $n
    i32.eq
    if
      i32.const 1
      return
    else
      i32.const 0
      return
    end
  )
  (func $classify (param $n i32) (result i32)
    local.get $n
    i32.const 0
    i32.lt_s
    if
      i32.const 1
      return
    else
      local.get $n
      i32.const 0
      i32.eq
      if
        i32.const 2
        return
      else
        local.get $n
        i32.const 10
        i32.lt_s
        if
          i32.const 3
          return
        else
          i32.const 4
          return
        end
      end
    end
  )
  (func $nested_loop_test (param $limit i32) (result i32) (local $i i32) (local $total i32) (local $j i32)
    i32.const 0
    local.set $i
    i32.const 0
    local.set $total
    block
      loop
        local.get $i
        local.get $limit
        i32.lt_s
        i32.eqz
        br_if 1
        i32.const 0
        local.set $j
        block
          loop
            local.get $j
            local.get $limit
            i32.lt_s
            i32.eqz
            br_if 1
            local.get $i
            local.get $j
            i32.ne
            if
              local.get $total
              local.get $i
              i32.add
              local.get $j
              i32.add
              local.set $total
            else
              local.get $total
              i32.const 1
              i32.add
              local.set $total
            end
            local.get $j
            i32.const 1
            i32.add
            local.set $j
            br 0
          end
        end
        local.get $i
        i32.const 1
        i32.add
        local.set $i
        br 0
      end
    end
    local.get $total
    return
  )
  (func $arithmetic_test (param $a i32) (param $b i32) (param $c i32) (result i32) (local $x i32) (local $y i32) (local $z i32) (local $w i32)
    local.get $a
    local.get $b
    local.get $c
    i32.mul
    i32.add
    local.set $x
    local.get $a
    local.get $b
    i32.add
    local.get $c
    i32.mul
    local.set $y
    local.get $a
    local.get $b
    i32.sub
    local.get $c
    i32.sub
    local.set $z
    local.get $a
    local.get $b
    i32.div_s
    local.set $w
    local.get $x
    local.get $y
    i32.add
    local.get $z
    i32.add
    local.get $w
    i32.add
    return
  )
  (func $logical_test (param $a i32) (param $b i32) (result i32)
    local.get $a
    i32.const 0
    i32.gt_s
    local.get $b
    i32.const 0
    i32.gt_s
    i32.and
    local.get $a
    i32.const 0
    i32.eq
    i32.or
    if
      i32.const 1
      return
    else
      i32.const 0
      return
    end
  )
  (func $string_pointer_test  (result i32)
    i32.const 0
    return
  )
  (func $calculate_score (param $base i32) (param $bonus i32) (param $penalty i32) (result i32) (local $score i32)
    local.get $base
    local.get $bonus
    i32.add
    local.get $penalty
    i32.sub
    local.set $score
    local.get $score
    i32.const 0
    i32.lt_s
    if
      i32.const 0
      return
    else
      local.get $score
      return
    end
  )
  (func $main (export "main")  (result i32) (local $a i32) (local $b i32) (local $c i32) (local $absolute i32) (local $maximum i32) (local $minimum i32) (local $fact i32) (local $fib i32) (local $divisor i32) (local $total i32) (local $even_result i32) (local $odd_result i32) (local $category_a i32) (local $category_b i32) (local $category_c i32) (local $category_d i32) (local $nested i32) (local $arithmetic i32) (local $logic_a i32) (local $logic_b i32) (local $score i32)
    i32.const 17
    local.set $a
    i32.const 5
    local.set $b
    i32.const 3
    local.set $c
    i32.const 0
    local.get $a
    i32.sub
    call $abs_value
    local.set $absolute
    local.get $a
    local.get $b
    call $max_value
    local.set $maximum
    local.get $a
    local.get $b
    call $min_value
    local.set $minimum
    i32.const 6
    call $factorial
    local.set $fact
    i32.const 10
    call $fibonacci
    local.set $fib
    i32.const 48
    i32.const 18
    call $gcd
    local.set $divisor
    i32.const 100
    call $sum_range
    local.set $total
    i32.const 42
    call $is_even
    local.set $even_result
    i32.const 17
    call $is_even
    local.set $odd_result
    i32.const 0
    call $classify
    local.set $category_a
    i32.const 7
    call $classify
    local.set $category_b
    i32.const 15
    call $classify
    local.set $category_c
    i32.const -4
    call $classify
    local.set $category_d
    i32.const 5
    call $nested_loop_test
    local.set $nested
    local.get $a
    local.get $b
    local.get $c
    call $arithmetic_test
    local.set $arithmetic
    i32.const 5
    i32.const 8
    call $logical_test
    local.set $logic_a
    i32.const 0
    i32.const 8
    call $logical_test
    local.set $logic_b
    i32.const 80
    i32.const 15
    i32.const 20
    call $calculate_score
    local.set $score
    local.get $fact
    i32.const 720
    i32.eq
    local.get $fib
    i32.const 55
    i32.eq
    i32.and
    if
      local.get $divisor
      i32.const 6
      i32.eq
      local.get $total
      i32.const 5050
      i32.eq
      i32.and
      if
        local.get $maximum
        i32.const 17
        i32.eq
        local.get $minimum
        i32.const 5
        i32.eq
        i32.and
        if
          local.get $score
          local.get $absolute
          i32.add
          local.get $nested
          i32.add
          local.get $arithmetic
          i32.add
          local.get $category_a
          i32.add
          local.get $category_b
          i32.add
          local.get $category_c
          i32.add
          local.get $category_d
          i32.add
          local.get $even_result
          i32.add
          local.get $odd_result
          i32.add
          local.get $logic_a
          i32.add
          local.get $logic_b
          i32.add
          return
        else
          i32.const 101
          return
        end
      else
        i32.const 102
        return
      end
    else
      i32.const 103
      return
    end
  )
)
