

-- -----------------------------------------------------
-- Table `skanban`.`board`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `board` (
  `idboard` INTEGER PRIMARY KEY,
  `title` TEXT NOT NULL ,
  `background` TEXT NULL ,
  `size_x` INT NOT NULL ,
  `size_y` INT NOT NULL);



-- -----------------------------------------------------
-- Table `skanban`.`postit`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `postit` (
  `idpostit` INTEGER PRIMARY KEY,
  `path` TEXT NULL ,
  `pos_x` INT NOT NULL ,
  `pos_y` INT NOT NULL ,
  `size_x` INT NOT NULL ,
  `size_y` INT NOT NULL ,
  `board_idboard` INT NOT NULL ,
  CONSTRAINT `fk_postit_board`
    FOREIGN KEY (`board_idboard` )
    REFERENCES `board` (`idboard` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

