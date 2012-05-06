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
					_rootDirectory = current.Split(new string[] { "\\util" }, StringSplitOptions.RemoveEmptyEntries)[0];
				}
				return _rootDirectory;
			}
		}

		public static bool Exists(string relativePathToRoot)
		{
			string path = CanonicalizePath(relativePathToRoot);
			return System.IO.File.Exists(path);
		}

		public static string ReadOrCreateBlank(string relativePathToRoot)
		{
			string path = CanonicalizePath(relativePathToRoot);
			if (System.IO.File.Exists(path))
			{
				return ReadFile(relativePathToRoot);
			}

			System.IO.File.WriteAllText(path, "");
			return "";
		}

		public static string CanonicalizePath(string relativePathToRoot)
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

		public static string[] GetFilesInFolder(string folderPath, bool fullPath)
		{
			string path = CanonicalizePath(folderPath);
			string[] output = System.IO.Directory.GetFiles(path);
			output = fullPath ? output : StripOffFullPaths(output);
			return output;
		}

		public static string[] GetFoldersInFolder(string folderPath, bool fullPath)
		{
			string path = CanonicalizePath(folderPath);
			string[] output = System.IO.Directory.GetDirectories(path);
			output = fullPath ? output : StripOffFullPaths(output);
			return output;
		}

		private static string[] StripOffFullPaths(string[] paths)
		{
			List<string> newPaths = new List<string>();
			foreach (string fullPath in paths)
			{
				string[] pieces = fullPath.Split('\\');
				string file = pieces[pieces.Length - 1];
				newPaths.Add(file);
			}
			return newPaths.ToArray();
		}
	}
}
