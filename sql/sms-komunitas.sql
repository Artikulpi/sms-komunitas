-- phpMyAdmin SQL Dump
-- version 3.3.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Waktu pembuatan: 06. Januari 2012 jam 16:59
-- Versi Server: 5.1.54
-- Versi PHP: 5.3.5-1ubuntu7.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `angkringan`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `latest`
--

CREATE TABLE IF NOT EXISTS `latest` (
  `last_sms` int(11) NOT NULL,
  `last_queue` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `latest`
--

INSERT INTO latest values(0,0);

DELIMITER |
CREATE TRIGGER updatelatest AFTER INSERT ON inbox
FOR EACH ROW BEGIN
    update latest set last_sms = NEW.ID;
END;
|
DELIMITER ;

