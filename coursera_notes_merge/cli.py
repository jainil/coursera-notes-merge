import click
import os
import fnmatch
from PyPDF2 import PdfFileMerger

merger = PdfFileMerger()

def traverse_dir(directory):
  count = 0
  for root, subdir, files in os.walk(directory):
    for item in fnmatch.filter(files, "*.pdf"):
      input_path = os.path.join(root, item)
      try:
        input = open(input_path, "rb")
        merger.append(input)
        click.echo('File {0} added'.format(input_path))
        input.close()
        count += 1
      except:
        click.echo('File {0} skipped.'.format(input_path))

  return count

@click.command()
@click.option('--output', '-o', default="notes.pdf", help='Name of output file.')
@click.argument('path', default='', required=False)
def main(path, output):
  """Merges course notes downloaded from coursera-dl"""
  cwd = os.path.join(os.getcwd(), path)
  output = os.path.join(cwd, output)

  if os.path.exists(output):
    click.echo('Deleting output file that already exists.')
    os.remove(output)

  count = traverse_dir(cwd)

  of = open(output, "wb")

  if count != 0:
    merger.write(of)
    click.echo('Notes merged into {0}'.format(output))
  else:
    click.echo('No notes found.')

  of.close()
