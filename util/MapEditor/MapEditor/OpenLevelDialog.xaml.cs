using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace MapEditor
{
	/// <summary>
	/// Interaction logic for OpenLevelDialog.xaml
	/// </summary>
	public partial class OpenLevelDialog : Window
	{
		public bool Status { get; private set; }
		public string Level { get; private set; }

		public OpenLevelDialog()
		{
			InitializeComponent();
			this.ok_button.Click += new RoutedEventHandler(ok_button_Click);
			this.cancel_button.Click += new RoutedEventHandler(cancel_button_Click);
			string[] files = FileStuff.GetFilesInFolder("data/levels", false);
			foreach (string file in files)
			{
				string name = file.EndsWith(".txt") ? file.Substring(0, file.Length - 4) : file;
				this.level_selector.Items.Add(name);
			}
			this.level_selector.SelectedIndex = 0;
			this.Status = false;
		}

		void cancel_button_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void ok_button_Click(object sender, RoutedEventArgs e)
		{
			this.Status = true;
			this.Level = this.level_selector.SelectedValue.ToString();
			this.Close();
		}
	}
}
