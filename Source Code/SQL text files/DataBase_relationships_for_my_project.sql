CREATE SCHEMA `quiz` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `quiz`.`user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(50) NULL DEFAULT NULL,
  `lastName` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(50) NULL,
  `salt` VARCHAR(512) NOT NULL,
  `passwordHash` VARCHAR(512) NOT NULL,
  `profile` INT(15) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_email` (`email` ASC) );

CREATE TABLE `quiz`.`quiz` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `hostId` BIGINT NOT NULL,
  `title` VARCHAR(75) NOT NULL,
  `type` SMALLINT(6) NOT NULL DEFAULT 0,
  `maxScore` SMALLINT(6) NOT NULL DEFAULT 0,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_quiz_host` (`hostId` ASC),
  CONSTRAINT `fk_quiz_host`
    FOREIGN KEY (`hostId`)
    REFERENCES `quiz`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    
CREATE TABLE `quiz`.`quiz_question` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `quizId` BIGINT NOT NULL,
  `type` VARCHAR(50) NOT NULL,
  `level` SMALLINT(6) NOT NULL DEFAULT 0,
  `score` SMALLINT(6) NOT NULL DEFAULT 0,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_question_quiz` (`quizId` ASC),
  CONSTRAINT `fk_question_quiz`
    FOREIGN KEY (`quizId`)
    REFERENCES `quiz`.`quiz` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE `quiz`.`quiz_answer` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `quizId` BIGINT NOT NULL,
  `questionId` BIGINT NOT NULL,
  `correct` TINYINT(1) NOT NULL DEFAULT 0,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_answer_quiz` (`quizId` ASC),
  CONSTRAINT `fk_answer_quiz`
    FOREIGN KEY (`quizId`)
    REFERENCES `quiz`.`quiz` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE `quiz`.`quiz_answer` 
ADD INDEX `idx_answer_question` (`questionId` ASC);
ALTER TABLE `quiz`.`quiz_answer` 
ADD CONSTRAINT `fk_answer_question`
  FOREIGN KEY (`questionId`)
  REFERENCES `quiz`.`quiz_question` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
CREATE TABLE `quiz`.`take` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `userId` BIGINT NOT NULL,
  `quizId` BIGINT NOT NULL,
  `score` SMALLINT(6) NOT NULL DEFAULT 0,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_take_user` (`userId` ASC),
  CONSTRAINT `fk_take_user`
    FOREIGN KEY (`userId`)
    REFERENCES `quiz`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE `quiz`.`take` 
ADD INDEX `idx_take_quiz` (`quizId` ASC);
ALTER TABLE `quiz`.`take` 
ADD CONSTRAINT `fk_take_quiz`
  FOREIGN KEY (`quizId`)
  REFERENCES `quiz`.`quiz` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
CREATE TABLE `quiz`.`take_answer` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `takeId` BIGINT NOT NULL,
  `questionId` BIGINT NOT NULL,
  `answerId` BIGINT NOT NULL,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_answer_take` (`takeId` ASC),
  CONSTRAINT `fk_answer_take`
    FOREIGN KEY (`takeId`)
    REFERENCES `quiz`.`take` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE `quiz`.`take_answer` 
ADD INDEX `idx_tanswer_question` (`questionId` ASC);
ALTER TABLE `quiz`.`take_answer` 
ADD CONSTRAINT `fk_tanswer_question`
  FOREIGN KEY (`questionId`)
  REFERENCES `quiz`.`quiz_question` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `quiz`.`take_answer` 
ADD INDEX `idx_tanswer_answer` (`answerId` ASC);
ALTER TABLE `quiz`.`take_answer` 
ADD CONSTRAINT `fk_tanswer_answer`
  FOREIGN KEY (`answerId`)
  REFERENCES `quiz`.`quiz_answer` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;