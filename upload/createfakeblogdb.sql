USE [master]
GO
/****** Object:  Database [FakeBlogDB]    Script Date: 10/1/2012 5:58:01 PM ******/
CREATE DATABASE [FakeBlogDB]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'FakeBlogDB', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\DATA\FakeBlogDB.mdf' , SIZE = 3072KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'FakeBlogDB_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\DATA\FakeBlogDB_log.ldf' , SIZE = 1024KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [FakeBlogDB] SET COMPATIBILITY_LEVEL = 110
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [FakeBlogDB].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [FakeBlogDB] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [FakeBlogDB] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [FakeBlogDB] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [FakeBlogDB] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [FakeBlogDB] SET ARITHABORT OFF 
GO
ALTER DATABASE [FakeBlogDB] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [FakeBlogDB] SET AUTO_CREATE_STATISTICS ON 
GO
ALTER DATABASE [FakeBlogDB] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [FakeBlogDB] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [FakeBlogDB] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [FakeBlogDB] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [FakeBlogDB] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [FakeBlogDB] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [FakeBlogDB] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [FakeBlogDB] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [FakeBlogDB] SET  DISABLE_BROKER 
GO
ALTER DATABASE [FakeBlogDB] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [FakeBlogDB] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [FakeBlogDB] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [FakeBlogDB] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [FakeBlogDB] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [FakeBlogDB] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [FakeBlogDB] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [FakeBlogDB] SET RECOVERY FULL 
GO
ALTER DATABASE [FakeBlogDB] SET  MULTI_USER 
GO
ALTER DATABASE [FakeBlogDB] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [FakeBlogDB] SET DB_CHAINING OFF 
GO
ALTER DATABASE [FakeBlogDB] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [FakeBlogDB] SET TARGET_RECOVERY_TIME = 0 SECONDS 
GO
EXEC sys.sp_db_vardecimal_storage_format N'FakeBlogDB', N'ON'
GO
USE [FakeBlogDB]
GO
/****** Object:  Table [dbo].[entries]    Script Date: 10/1/2012 5:58:01 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[entries](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[entryTitle] [varchar](50) NOT NULL,
	[createdById] [bigint] NOT NULL,
	[viewCount] [int] NOT NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[Users]    Script Date: 10/1/2012 5:58:01 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[Users](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[username] [varchar](20) NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
USE [master]
GO
ALTER DATABASE [FakeBlogDB] SET  READ_WRITE 
GO

insert into fakeblog.users (username) values ('userOne');
insert into fakeblog.users (username) values ('userTwo');
insert into fakeblog.entries (entrytitle, createdbyid, viewcount)
values ('entry one', 1, 0);
insert into fakeblog.entries (entrytitle, createdbyid, viewcount)
values ('entry two', 1, 10);
insert into fakeblog.entries (entrytitle, createdbyid, viewcount)
values ('entry three', 2, 5);
insert into fakeblog.entries (entrytitle, createdbyid, viewcount)
values ('entry four', 1, 500);