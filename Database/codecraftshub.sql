-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2024 at 12:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `codecrafthub`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `srl_num` int(50) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_num` varchar(50) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`srl_num`, `name`, `email`, `phone_num`, `msg`, `date`) VALUES
(1, 'Muhammad Hasnain Shahid', 'm347hasnain@gmail.com', '03124250355', 'I am a Software Engineer.', '2024-01-12 18:42:15'),
(2, 'Ali Raza', 'aliraza@gmail.com', '123456789', 'Flask developer', '2024-01-12 18:57:46');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `srl_num` int(50) NOT NULL,
  `title` text NOT NULL,
  `tagline` text NOT NULL,
  `slug` varchar(30) NOT NULL,
  `content` text NOT NULL,
  `img_file` varchar(20) NOT NULL DEFAULT '',
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`srl_num`, `title`, `tagline`, `slug`, `content`, `img_file`, `date`) VALUES
(1, ' A Guide to the Latest Technologies Using Python', 'Unleashing Innovation with Python\'s Powerful Arsenal', 'first-post', 'Introduction:\r\nPython, known for its versatility and readability, continues to be at the forefront of technological innovation. In this blog post, we embark on a journey to explore the latest technologies that leverage the power of Python. From machine learning and artificial intelligence to web development and beyond, discover how Python is shaping the technological landscape.', 'post1-bg.jpg', '2024-01-01 19:52:58'),
(2, 'Second post.', 'second post tagline', 'second-post', 'FastAPI: Modern, Fast, and (Asynchronous) Pythonic\r\nFastAPI is a web framework designed for building APIs quickly and efficiently. Leveraging Python\'s type hints, it offers automatic OpenAPI and JSON Schema generation. With support for asynchronous programming, FastAPI excels in creating high-performance web applications.', 'tech-bg.jpg', '2023-12-28 16:34:56'),
(3, 'Third post', 'third post tagline.', 'third-post', 'Kubernetes: Orchestrating Scalable Applications\r\nKubernetes, the go-to solution for container orchestration, relies on Python for managing and deploying applications at scale. Its extensibility and community support make it the preferred choice for scalable and resilient systems.', 'tech-bg.jpg', '2024-01-02 20:07:00'),
(4, 'Fourth post', 'fourth post tagline.', 'fourth-post', 'Django Channels: Real-Time Web Applications\r\nDjango Channels extends Django\'s capabilities to handle real-time functionality. By introducing WebSockets, it empowers developers to build responsive and interactive web applications, positioning it as a formidable choice for projects with real-time requirements.', '', '2023-12-28 17:02:34');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(80) NOT NULL,
  `user_email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `password`) VALUES
(1, 'test', 'test@email.com', '$2b$12$Pdj7bGhEbOjdWg99ozFiVeLuhIIBeeGe1v9KFkBnNayO8if1WszOa'),
(2, 'M Husnain', 'husnain@gmail.com', '$2b$12$54KLEd573wuybEIDCeS6g.JFApv1GVioABre6aAXjABRXNk5QKusO');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`srl_num`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`srl_num`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `srl_num` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `srl_num` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
