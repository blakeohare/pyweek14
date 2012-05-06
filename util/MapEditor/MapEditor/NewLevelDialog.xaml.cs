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
	/// Interaction logic for NewLevelDialog.xaml
	/// </summary>
	public partial class NewLevelDialog : Window
	{
		public bool Status { get; private set; }
		public string LevelName { get; private set; }

		public NewLevelDialog()
		{
			InitializeComponent();
			this.Status = false;
			this.ok_button.Click += new RoutedEventHandler(ok_button_Click);
			this.cancel_button.Click += new RoutedEventHandler(cancel_button_Click);
		}

		void cancel_button_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void ok_button_Click(object sender, RoutedEventArgs e)
		{
			this.Status = true;
			this.LevelName = this.level_name.Text.Trim();
			this.Close();
		}
	}
}
