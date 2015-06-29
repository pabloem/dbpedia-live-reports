========================================
State of the Live DBPedia updates
========================================

:Author: Pablo Estrada <pablo(at)snu(dot)ac(dot)kr>
:Date: Jun 17, 2015

Introduction
==========================================
This report is written as part of the Google Summer of Code-sponsored project
'Adding Liveness to the Linked Data Fragments Server'. The goal of this report
is to characterize the rate of updates to the Live DBPedia, to estimate 
appropriate parameters to run the Linked Data Fragments Server.
Before anything, we shall load the data.
<<echo=False>>=
import pandas
import numpy as np
import matplotlib.pyplot as plt
@
<<>>=
#df = pandas.read_json('scrape_results.json')
df = pandas.read_csv('changesetInfo.csv')
df['changesets'] = 1
res = df['url'].str.split('/')
df['url_date'] = res.str[4]+'/'+res.str[5]+'/'+res.str[6]+' '+res.str[7]+':00'
#df['url_date'] = 1
df_p_hour = df.groupby('url_date').sum()
@

How many triples?
------------------------------------------
First of all, we can see that the average number of triples per changeset is 
**<%print("%.2f" % df['triples'].mean())%>**; while the average number of 
triples per hour is **<%print("%.2f" % df_p_hour['triples'].mean())%>**; 
although these means may vary over time, as more data is collected. Also, 
the average number of changesets per hour is **<%print("%.2f" % df_p_hour['changesets'].mean())%>**. 
Note that these numbers are for both added, and removed triples.

On the following charts, we observe histograms of the number of triples per 
hour and per changeset. It should be noted also, that the following charts 
are in logarithmic or linear scales, depending on convenience. Pay close 
attention to the scales, so as not to be confused.

<<>>=
# Histogram of number of triples per changeset
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
mx = df['triples'].max()
ax.set_title('Triples per changeset (histogram)')
ax.set_xlabel('Number of triples')
ax.set_ylabel('Number of changesets')
ax.set_xscale('log')
df['triples'].hist(log=True,bins=np.logspace(0, 1, base=mx, num=50))
plt.axvline(df['triples'].mean(),color='r')

# Histogram of number of triples per hour
# Number of changesets per changeset. This will be useful later on.
fig = plt.figure()
ax = fig.add_subplot(111)

df_p_hour['triples'].hist(bins=20)
plt.axvline(df_p_hour['triples'].mean(),color='r')
ax.set_title('Triples per hour (Histogram)')
ax.set_xlabel('Number of triples')
ax.set_ylabel('Number of hours')
@

As we see, the number of triples per changeset...

<<fig = True, width = '20 cm', echo=True>>=
fig = plt.figure()
fig.suptitle('Behavior of changesets over time')
fig.set_size_inches(1,1)
ax = fig.add_subplot(3,1,1)
ax.get_xaxis().set_visible(False)
ax.set_ylabel('#Triples/Changeset')
ax.set_xlabel('Hours since Midnight, Jan 1, 2014')
(df_p_hour['triples']/df_p_hour['changesets']).plot(kind='bar',log=True)
plt.axhline((df['triples']/df['changesets']).mean(),color='r')

ax = fig.add_subplot(3,1,2)
ax.get_xaxis().set_visible(False)
ax.set_ylabel('#Changesets/Hour')
ax.set_xlabel('Hours since Midnight, Jan 1, 2014')
df_p_hour['changesets'].plot(kind='bar',log=True)
plt.axhline(df_p_hour['changesets'].mean(),color='r')

ax = fig.add_subplot(3,1,3)
ax.set_ylabel('#Triples/Hour')
df_p_hour['triples'].plot(kind='bar').set_xlabel('Hours since Midnight, Jan 1, 2014')
plt.axhline(df_p_hour['triples'].mean(),color='r')

ticks = ['' for i in range(len(df_p_hour['triples']))]
ticks[-1] = len(df_p_hour['triples'])
ax.set_xticklabels(ticks)
@

A more detailed view of the per-hour behavior:
<<echo=False>>=
print(df_p_hour)
@


