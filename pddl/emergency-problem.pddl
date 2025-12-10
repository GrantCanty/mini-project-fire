(define (problem emergency-evacuation)
  (:domain evacuation)

  (:objects
    ;; robots
    robot1 robot2 - robot

    ;; people
    p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 - person

    ;; rooms
    office-a office-b office-c corridor-2
    room-1 room-2 room-3 corridor-1
    hall reception exit
    stairs-left stairs-right - room

    ;; floors (not used yet, but allowed by domain)
    floor-1 floor-2 ground - floor
  )

  (:init
    ;; -------------------------
    ;; initial robot positions
    ;; -------------------------
    (robot-in robot1 hall)
    (robot-in robot2 reception)
    (free robot1)
    (free robot2)

    ;; -------------------------
    ;; initial people positions
    ;; -------------------------
    ;; 3 people in Office-A (Floor 2)
    (person-in p1 office-a)
    (person-in p2 office-a)
    (person-in p3 office-a)

    ;; 2 people in Office-C (Floor 2)
    (person-in p4 office-c)
    (person-in p5 office-c)

    ;; 2 people in Room-1 (Floor 1)
    (person-in p6 room-1)
    (person-in p7 room-1)

    ;; 2 people in Room-3 (Floor 1)
    (person-in p8 room-3)
    (person-in p9 room-3)

    ;; 1 person in Hall (Ground)
    (person-in p10 hall)

    ;; -------------------------
    ;; smoky and safe rooms
    ;; -------------------------
    ;; smoky zones (danger)
    (smoky office-b)
    (smoky room-2)

    ;; all other rooms are safe for moving with a person
    (safe office-a)
    (safe office-c)
    (safe corridor-2)
    (safe room-1)
    (safe room-3)
    (safe corridor-1)
    (safe hall)
    (safe reception)
    (safe exit)
    (safe stairs-left)
    (safe stairs-right)

    ;; -------------------------
    ;; exit
    ;; -------------------------
    (is-exit exit)

    ;; -------------------------
    ;; connectivity (bidirectional)
    ;; Floor 2
    ;; -------------------------
    (connected office-a office-b)
    (connected office-b office-a)

    (connected office-b corridor-2)
    (connected corridor-2 office-b)

    (connected corridor-2 office-c)
    (connected office-c corridor-2)

    ;; stairs from floor 2 down
    (connected office-a stairs-left)
    (connected stairs-left office-a)

    (connected office-c stairs-right)
    (connected stairs-right office-c)

    ;; -------------------------
    ;; Floor 1
    ;; -------------------------
    (connected room-1 room-2)
    (connected room-2 room-1)

    (connected room-2 corridor-1)
    (connected corridor-1 room-2)

    (connected corridor-1 room-3)
    (connected room-3 corridor-1)

    ;; vertical connections floor1 <-> ground
    (connected room-1 hall)
    (connected hall room-1)

    (connected room-3 reception)
    (connected reception room-3)

    ;; stairs connect floor1 & floor2 via ground
    (connected hall stairs-left)
    (connected stairs-left hall)

    (connected reception stairs-right)
    (connected stairs-right reception)

    ;; optional connection between the two stairs (bottom link)
    (connected stairs-left stairs-right)
    (connected stairs-right stairs-left)

    ;; -------------------------
    ;; Ground floor
    ;; -------------------------
    (connected hall reception)
    (connected reception hall)

    (connected reception exit)
    (connected exit reception)
  )

  (:goal
    (and
      (evacuated p1)
      (evacuated p2)
      (evacuated p3)
      (evacuated p4)
      (evacuated p5)
      (evacuated p6)
      (evacuated p7)
      (evacuated p8)
      (evacuated p9)
      (evacuated p10)
    )
  )
)
