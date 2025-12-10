(define (domain evacuation)
  (:requirements :strips :typing)
  (:types
    robot person room floor - object
  )

  (:predicates
    ;; positions
    (robot-in ?r - robot ?s - room)
    (person-in ?p - person ?s - room)

    ;; robot load status
    (free ?r - robot)
    (carrying ?r - robot ?p - person)

    ;; map & environment
    (connected ?from - room ?to - room)
    (smoky ?s - room)
    (safe ?s - room)                 ; non-smoky rooms allowed with a person
    (is-exit ?s - room)

    ;; goal
    (evacuated ?p - person)
  )

  ;; --------------------
  ;; move robot alone
  ;; --------------------
  (:action move-robot-empty
    :parameters (?r - robot ?from - room ?to - room)
    :precondition (and
      (robot-in ?r ?from)
      (free ?r)
      (connected ?from ?to)
    )
    :effect (and
      (robot-in ?r ?to)
      (not (robot-in ?r ?from))
    )
  )

  ;; --------------------
  ;; move robot carrying a person
  ;; (only into safe rooms, to avoid smoke)
  ;; --------------------
  (:action move-robot-loaded
    :parameters (?r - robot ?p - person ?from - room ?to - room)
    :precondition (and
      (robot-in ?r ?from)
      (carrying ?r ?p)
      (connected ?from ?to)
      (safe ?to)
    )
    :effect (and
      (robot-in ?r ?to)
      (not (robot-in ?r ?from))
    )
  )

  ;; --------------------
  ;; pick up a person
  ;; --------------------
  (:action pick-up
    :parameters (?r - robot ?p - person ?loc - room)
    :precondition (and
      (robot-in ?r ?loc)
      (person-in ?p ?loc)
      (free ?r)
    )
    :effect (and
      (carrying ?r ?p)
      (not (person-in ?p ?loc))
      (not (free ?r))
    )
  )

  ;; --------------------
  ;; drop a person at the EXIT
  ;; --------------------
  (:action drop-at-exit
    :parameters (?r - robot ?p - person ?loc - room)
    :precondition (and
      (robot-in ?r ?loc)
      (carrying ?r ?p)
      (is-exit ?loc)
    )
    :effect (and
      (evacuated ?p)
      (free ?r)
      (not (carrying ?r ?p))
    )
  )
)
