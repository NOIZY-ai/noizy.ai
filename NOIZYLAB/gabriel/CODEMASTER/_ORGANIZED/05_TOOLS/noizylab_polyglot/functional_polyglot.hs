{- Haskell / ML / OCaml / F# Polyglot -}
-- Haskell sees this as valid
-- Other ML-family languages handle differently

{-# LANGUAGE CPP #-}

#if 0
-- OCaml section
let () = print_endline "OCaml"
#endif

main :: IO ()
main = putStrLn "Haskell"

{-
(* OCaml *)
let () = print_endline "OCaml"

(* F# *)
printfn "F#"

(* Standard ML *)
print "SML\n"

(* Reason *)  
print_endline("Reason");
-}
