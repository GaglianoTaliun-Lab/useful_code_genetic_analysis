##Code from Daniel Taliun

##pipeline description
#run epacts script without run flag, so just makes the make file
#./Script-epacts-LDL.sh

#set up scripts
#python epacts2slurm.py --in-makefile epacts-LDL.Makefile --job-name LDL --max-mem 4000

#submit to queue 
#./run.LDL.sh 

###
import os
import stat
import sys
import argparse

argparser = argparse.ArgumentParser(description = 'Transforms EPACTS Makefile to SLURM jobarray with dependencies.')
argparser.add_argument('--in-makefile', metavar = 'Makefile', dest = 'inMakefile', required = True, help = 'Input EPACTS Makefile name.')
argparser.add_argument('--job-name', metavar = 'name', dest = 'jobName', required = True, help = 'SLURM array job name.')
argparser.add_argument('--partition', metavar = 'name(s)', dest = 'slurmPartition', required = True, help = 'SLURM partition name.')
argparser.add_argument('--max-mem', metavar = 'number', dest = 'maxMem', required = True, help = 'Maximum memory per job in MB.')

def parseMakefile(inMakefile):
   with open(inMakefile, 'r') as ifile:
      rules = dict()
      isRule = False
      target = None
      for line in ifile:
         line = line.rstrip()
         if not line:
            isRule = False
            continue

         if line.startswith('\t'):
            if not isRule:
               raise Exception("Error while parsing a rule: unexpected tab character")
            rules[target]['recipe'].append(line.strip())
         else:
            if line.count(':') == 0:
               raise Exception("Error while parsing a rule: no colon in target and prerequisites line")
            elif line.count(':') > 1:
               raise Exception("Error while parsing a rule: >1 colons in target and prerequisites line")

            target, prerequisites = [x.strip() for x in line.split(':')]

            if target in rules:
               raise Exception("Error while parsing a rule: duplicated target")

            rules[target] = {'prerequisites': set(), 'recipe': list()}

            for prerequisite in prerequisites.split(' '):
               rules[target]['prerequisites'].add(prerequisite)
            isRule = True
      return rules

def getSlurmJobTargets(rules, used_targets):
   jobs = list()

   for target, rule in rules.iteritems():
      if target.startswith('.') or target == 'clean' or target == 'all':
         continue

      if target in used_targets:
         continue

      if len(used_targets) == 0:
         depends_on = False
         for prerequisite in rule['prerequisites']:
            if prerequisite in rules:
               depends_on = True
               break
         if not depends_on:
            jobs.append(target)
      else:
         depends_on = True
         for prerequisite in rule['prerequisites']:
            if prerequisite not in rules:
               continue
            if prerequisite not in used_targets:
               depends_on = False
               break
         if depends_on:
            jobs.append(target)
   return jobs

def writeSlurmJob(targets, jobid, jobname):
   filename = str(jobid) + "." + jobname + ".sbatch"
   with open(filename, 'w') as ofile:
      ofile.write("#!/bin/bash\n\n")
      if len(targets) > 1:
         ofile.write("#SBATCH --array=0-%d\n" % (len(targets) - 1))
         ofile.write("#SBATCH --job-name=%d.%s\n" % (jobid, jobname))
         ofile.write("#SBATCH --output=%d.%s-%%a.log\n" % (jobid, jobname))
         ofile.write("\n")
         ofile.write("declare -a jobs\n")
         ofile.write("\n")
         for i in xrange(0, len(targets)):
            ofile.write('jobs[%d]="' % i)
            for recipe in rules[targets[i]]['recipe']:
               ofile.write('%s ;' % recipe)
            ofile.write('"\n')
         ofile.write("\n")
         ofile.write("${jobs[${SLURM_ARRAY_TASK_ID}]}\n")
      else:
         ofile.write("#SBATCH --job-name=%d.%s\n" % (jobid, jobname))
         ofile.write("#SBATCH --output=%d.%s.log\n" % (jobid, jobname))
         ofile.write("\n")
         for recipe in rules[targets[0]]['recipe']:
            ofile.write('%s\n' % recipe)

def writeSlurmJobSubmissionScript(jobs, jobname, partition, maxmem):
   filename = "run." + jobname + ".sh"
   with open(filename, 'w') as ofile:
      ofile.write("#!/bin/bash\n\n")

      ofile.write('echo "%d job(s) will be submitted into Slurm queue."\n\n' % len(jobs))

      for jobid in xrange(1, len(jobs) + 1):
         if jobid == 1:
            ofile.write('message=$(sbatch -p %s --mem=%s --time=14-0 %s)\n' % (partition, maxmem, str(jobid) + "." + jobname + ".sbatch"))
         else:
            ofile.write('message=$(sbatch -p %s --mem=%s --time=14-0 --depend=afterok:${job} %s)\n' % (partition, maxmem, str(jobid) + "." + jobname + ".sbatch"))

         ofile.write('if ! echo ${message} | grep -q "[1-9][0-9]*$"\n')
         ofile.write('then\n')
         ofile.write('\techo "Submission failed for job %d."\n' % jobid)
         ofile.write('\texit 1\n')
         ofile.write('fi\n\n')

         ofile.write('job=$(echo ${message} | grep -oh  "[1-9][0-9]*$")\n')
         if (len(jobs[jobid]) > 1):
            ofile.write('echo "Slurm job #%d (jobarray with %d jobs) was successfully submitted to Slurm queue with ID=${job}."\n' % (jobid, len(jobs[jobid])))
         else:
            ofile.write('echo "Slurm job #%d was successfully submitted to Slurm queue with ID=${job}."\n' % jobid)

         ofile.write('\n')
   filestat = os.stat(filename)
   os.chmod(filename, filestat.st_mode | stat.S_IEXEC)

def createSlurmJobs(rules, jobname, partition, maxmem):
   targets = list()
   jobid = 0
   used_targets = list()
   jobs = dict()
   while True:
      targets = getSlurmJobTargets(rules, used_targets)
      if len(targets) == 0:
          break
      used_targets.extend(targets)
      jobid += 1
      jobs[jobid] = list(targets)

   for jobid, targets in jobs.iteritems():
      writeSlurmJob(targets, jobid, jobname)

   writeSlurmJobSubmissionScript(jobs, jobname, partition, maxmem)

if __name__ == '__main__':
   args = argparser.parse_args()
   rules = parseMakefile(args.inMakefile)
   createSlurmJobs(rules, args.jobName, args.slurmPartition, args.maxMem)
