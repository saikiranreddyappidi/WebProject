#!/usr/bin/env python3

import os, glob

class BR(object):
  def __init__(self, output, test, indexes, directory, pattern, title):
    self.output = output
    self.test = test
    self.indexes = indexes
    self.begin = int(indexes.split(':')[0])
    self.end = int(indexes.split(':')[1])
    self.directory = directory
    self.pattern = pattern
    self.title = title
  
  def __str__(self):
    return 'BR(output={0}, test={1}, indexes={2}, directory={3}, pattern={4}, title={5})'.format(
      self.output, self.test, self.indexes, self.directory, self.pattern, self.title
    )
  
  def rename(self):
    if not os.path.isdir(self.directory):
      raise OSError('directory {} does not exist'.format(self.directory))
    for files in glob.iglob(os.path.join(self.directory, self.pattern)):
      title, ext = os.path.splitext(os.path.basename(files))
      if self.begin > self.end or self.begin > len(title):
        raise IndexError('begin index of {} is out of range'.format(self.begin))
      elif self.end > len(title):
        raise IndexError('end index of {} is out of range'.format(self.end))
      if not self.test:
        os.rename(files, os.path.join(self.directory, title[0:self.begin] + self.title + title[self.end:] + ext))
      if self.output:
        print(title + ext + ' -> ' + title[0:self.begin] + self.title + title[self.end:] + ext)
  
