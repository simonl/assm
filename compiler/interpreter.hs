
-- Types used :

-- data Exp = Ind Int 
--	 | Lam Exp 
--	 | App Exp Exp

--data Continuation = Argument Data 
--		  | Update Int 
--		  | Cases (Closure Cases)

--data Handle = Void 
--	    | Thunk (Closure Exp) 
--	    | Evaled (Closure Exp)

--type Closure a = (a, Env)
--type Case = Exp
-- type Cases = [Case]

-- data Data = Bits Int 
--	  | Reference Exp 
--	  | Pointer Int

--type Env = [Data]
--type Stack = [Continuation]
--type Heap = [Handle]

--type State = (Data, Env, Stack, Heap)
--type Action = State -> State


-- Interpreter (Horrible version) :

data Cont = Pointer Int | Update Int deriving Show
data Exp = Ind Int | Lam Exp | App Exp Exp

instance Show Exp where
	show (Lam e)   = "\\" ++ show e
	show (App f x) = "(" ++ show f ++ " " ++ show x ++ ")"
	show (Ind n)   = show n 

type Env = [Int]
type Stack = [Cont]
type Heap = [(Exp, Env)]

type State = (Exp, Env, Stack, Heap)

getExp   :: State -> Exp
getEnv   :: State -> Env
getStack :: State -> Stack
getHeap  :: State -> Heap

getExp   (e, _, _, _) = e
getEnv   (_, v, _, _) = v
getStack (_, _, s, _) = s
getHeap  (_, _, _, h) = h

input :: Exp
input = App (Lam $ Ind 0) $ Lam $ Lam $ Ind 1

initialState :: State
initialState = (input, [], [], []) 

main = putStrLn . concat . annotate 0 $ map (flip (++) "\n" . show . getExp) $ interpret initialState 

annotate :: Int -> [String] -> [String]
annotate n []     = []
annotate n (x:xs) = (show n ++ " : " ++ x) : annotate (n+1) xs

-- mutate :: Int -> Handle -> Heap -> Heap
mutate n e [] = error "position cannot be reference!"
mutate 0 e (x:xs) = e:xs
mutate n e (x:xs) = x : mutate (n-1) e xs

interpret :: State -> [State]
interpret s@(exp, env, stack, heap) =  s : stateInit exp env stack heap

stateInit :: Exp -> Env -> Stack -> Heap -> [State]
stateInit (App f x) env stack heap = interpret (f, env, stack', heap')
	where	stack' = (Pointer $ length heap) : stack
		heap'  = heap ++ [(x, env)]

stateInit (Ind n) env stack heap = interpret (exp', env', stack', heap)
	where	(exp', env') = heap !! (env !! n)
		stack' = Update n : stack

stateInit exp       env []     heap = [(exp, env, [], heap)]
stateInit (Lam exp) env (s:ss) heap = case s of
	(Pointer n) -> interpret (exp, n:env, ss, heap)
	(Update  n) -> interpret (expr, env, ss, heap')
		where	closed = (expr, env)
			heap' = mutate n closed heap
			expr = (Lam exp)


-- \E | (f x) | N
-- 4 instruction machine, 3 registers : code + env + cont | heap
--	(f a)	env	cont		heap
--	f	env	*:cont		heap++(a,env)

--	\E	env	*:cont		heap
--	E	*:env	cont		heap

--	\E	env	#:cont		heap
--	\E	env	cont		heap[#]=(\E,env)

--	N	[..N:*]	  cont		heap
--	*	_	  cont		heap
--	heap[*]	heap[**]  #:cont	heap

-- ... | {t} | (t,vs)
-- + Data Constructors (really just tuples)
--	case e of alt*	[]	cont			heap
--	e		[]	(alt*, []):cont		heap

--	{t}		[vs]	cont			heap
--	(t,vs)		_	cont			heap

--	(,)		[vs]	cont			heap 	-- Not now...
--	(vs)		_	cont			heap

--	(t,vs)		_	(alt*, []):cont		heap
--	alts[t]		[]	(t,vs):cont		heap
--	alt[t]		[*]	cont			heap++(t,vs)

--	(t,vs)		_	#:cont			heap
--	(t,vs)		_	cont			heap[#]=(t,vs)

