using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace MapEditor
{
	public static class FileStuff
	{

		private static string _rootDirectory = null;
		public static string RootDirectory
		{
			get
			{
				if (_rootDirectory == null)
				{
					string current = System.IO.Directory.GetCurrentDirectory();
					_rootDirectory = current.Split(new string[] { "util" }, StringSplitOptions.RemoveEmptyEntries)[0];
				}
				return _rootDirectory;
			}
		}

		private static string CanonicalizePath(string relativePathToRoot)
		{
			if (!relativePathToRoot.StartsWith("\\"))
			{
				relativePathToRoot = "\\" + relativePathToRoot;
			}
			return (RootDirectory + relativePathToRoot).Replace('/', '\\');
		}

		public static string ReadFile(string relativePathToRoot)
		{
			string path = CanonicalizePath(relativePathToRoot);
			return System.IO.File.ReadAllText(path);
		}

		public static void WriteFile(string relativePathToRoot, string contents)
		{
			string path = CanonicalizePath(relativePathToRoot);
			System.IO.File.WriteAllText(path, contents);
		}

		public static string[] GetFilesInFolder(string folderPath)
		{
			string path = CanonicalizePath(folderPath);
			return System.IO.Directory.GetFiles(path);
		}

		public static string[] GetFoldersInFolder(string folderPath)
		{
			string path = CanonicalizePath(folderPath);
			return System.IO.Directory.GetDirectories(path);
		}
	}
}
