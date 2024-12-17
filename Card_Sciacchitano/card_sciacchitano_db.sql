-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:4306
-- Creato il: Apr 03, 2024 alle 19:30
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `card_sciacchitano_db`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `carte`
--

CREATE TABLE `carte` (
  `id_carta` int(11) NOT NULL,
  `credito` float NOT NULL,
  `stato` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `carte`
--

INSERT INTO `carte` (`id_carta`, `credito`, `stato`) VALUES
(1, 32, 'attiva'),
(2, 120, 'attiva'),
(3, 102, 'non attiva'),
(4, 134, 'attiva'),
(5, 2528, 'non attiva'),
(6, 7883200, 'attiva'),
(7, 567, 'non attiva'),
(8, 584, 'attiva'),
(9, 787878, 'attiva'),
(10, 76876, 'attiva'),
(11, 156, 'attiva'),
(12, 77, 'attiva'),
(13, 980, 'attiva');

-- --------------------------------------------------------

--
-- Struttura della tabella `transazioni`
--

CREATE TABLE `transazioni` (
  `id_transazione` int(11) NOT NULL,
  `cod_utente` int(11) NOT NULL,
  `data` date NOT NULL,
  `importo` float NOT NULL,
  `cod_carta` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `transazioni`
--

INSERT INTO `transazioni` (`id_transazione`, `cod_utente`, `data`, `importo`, `cod_carta`) VALUES
(1, 2, '2024-03-13', 12, 1),
(2, 2, '2024-03-13', 22, 3),
(3, 2, '2024-03-13', 2323, 5),
(4, 1, '2024-03-13', -10, 4),
(5, 3, '2024-03-13', 88, 8),
(6, 3, '2024-03-13', 52, 8),
(7, 1, '2024-03-26', 90, 2),
(8, 2, '2024-03-26', -10, 2),
(9, 3, '2024-03-26', 7889990, 6),
(10, 1, '2024-04-03', 33, 11),
(11, 2, '2024-04-03', -6789, 6),
(12, 3, '2024-04-03', 44, 4);

--
-- Trigger `transazioni`
--
DELIMITER $$
CREATE TRIGGER `updatecarta` AFTER INSERT ON `transazioni` FOR EACH ROW UPDATE carte
    SET carte.credito = carte.credito + new.importo 
    WHERE carte.id_carta=new.cod_carta
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struttura della tabella `utenti`
--

CREATE TABLE `utenti` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `ruolo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `utenti`
--

INSERT INTO `utenti` (`id`, `email`, `name`, `password`, `ruolo`) VALUES
(1, 'Marco@email.it', 'Marco', '$2b$12$RiQ2caAWVD19EXOLlgz74uKdec7qv5b2k0AoEMNhn.9b.Kp9DAYka', 'ADMIN'),
(2, 'Alice@email.it', 'Alice', '$2b$12$jOseyNqkLiOw4gWNNRSrFeb4FjUMeExmm7M2JzwvEcFMW4AouMGQ2', 'NEGOZIANTE'),
(3, 'bob@emal.it', 'Bob', '$2b$12$ujGJVDnXRJvcwfUAr16qnuIhyMP2e4LLcI8riC2XsiqzwVrdgdK7C', 'NEGOZIANTE');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `carte`
--
ALTER TABLE `carte`
  ADD PRIMARY KEY (`id_carta`);

--
-- Indici per le tabelle `transazioni`
--
ALTER TABLE `transazioni`
  ADD PRIMARY KEY (`id_transazione`),
  ADD KEY `cod_carta` (`cod_carta`),
  ADD KEY `cod_utente` (`cod_utente`);

--
-- Indici per le tabelle `utenti`
--
ALTER TABLE `utenti`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `carte`
--
ALTER TABLE `carte`
  MODIFY `id_carta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT per la tabella `transazioni`
--
ALTER TABLE `transazioni`
  MODIFY `id_transazione` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT per la tabella `utenti`
--
ALTER TABLE `utenti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `transazioni`
--
ALTER TABLE `transazioni`
  ADD CONSTRAINT `carta` FOREIGN KEY (`cod_carta`) REFERENCES `carte` (`id_carta`),
  ADD CONSTRAINT `utente` FOREIGN KEY (`cod_utente`) REFERENCES `utenti` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
