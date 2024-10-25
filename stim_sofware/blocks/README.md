Each block corresponds to the *trial*, namely the sequence of 72 (12*6) syllables which are to be rythmically presented, the csv file has the following fields:

- SYLL, the syllable in uppercase (utf8 encoding of accented chars)	
- WP, word position within a sentence, when presented (1 to 6)
- TYPE,  type of sentence for mixed bloscks, for others (compular and control) is zero
- ORDER, order of the sentence (or group of 6 syllables) within the block
- TARGET, the bisyllabbic target word to be tested in the task at the end of the presentation 
- PRESENT, 1 if the target sequence is present in the stream, 0 otherwise

Ten blocks are available for each of the following 4 conditions, the file name has the format b[i].csv where i is the block number which identifies the condition and item. The same number will be used as tgrigger code in the EEG,  end of block will be marked with i+100 :
- COPULAR, all copular structures,i=11-20
- MIXED,  mixed structure , i=21-30
- COPULAR_CTR, randomization of copular sequences, i= 31-40
- MIXED_CTR, randomization of MIXED sequences, i= 41-50

Practice blocks are:
- p61.csv (copular)
- p71.csv (mixed)
- p81.csv (copular control)
- p91.csv (mixed control)

Four random lists of blocks have been generated with the following R code:

> set.seed(8832)
> sample(11:50)
> sample(11:50)
> sample(11:50)
> sample(11:50)

and are stored in the files:
- listA.txt
- listB.txt
- listC.txt
- listD.txt

Practice sequence will be fixed for all subjects (61,91,71,81), see pract.txt

In the file taskdescription.txt you'll find a  resume of the target words for each block and if it was present or not. Target in the task (and its presence) is always the same for a given block, independently from list.
