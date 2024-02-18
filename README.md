# ScalarTux

[![wakatime](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018cfe88-ac17-4fec-beee-9b65729eff00.svg)](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018cfe88-ac17-4fec-beee-9b65729eff00)

A game for our beloved Tux mascot where he needs to escape the rise of windows by scaling itself.

The game is still under development wait for any news.

Rules for Contribution:

When you want to push your changes to the main branch you must check these to do so:
|TypeChecker (mypy) Spits out ok reasonable errors:    | :white_check_mark:        |
|------------------------------------------------------|--------|
| The code works as your last commit intended to do:   |   :white_check_mark:     |
| Unit tests pass without a problem:                   |   :x:     |

There are no unit tests, yet

( :x: , :white_check_mark: )


TODO:

- Change the way that hitbox is the same as core x of the entity
- Redo x, y system for entities
  - Abstraction of the hitbox x, y coordinates
- Abstraction of the rectangle collision detector.
- Make `settings.py` load the settings from `settings.json`
