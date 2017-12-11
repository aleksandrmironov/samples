import hudson.model.*
import groovy.json.*

def build = Thread.currentThread().executable
def releaseType = build.buildVariableResolver.resolve("releaseType")
dev gitRepository = build.buildVariableResolver.resolve("gitRepository")

def get_next_release_version(releaseType, gitRepository){
  def cmd = "git ls-remote -t ${gitRepository}"
  def tags = cmd.execute()
                       .text.readLines()
                       .collect { it.split()[1].replaceAll('refs/tags/', '')  }
                       .collect { it.replaceAll("\\^\\{\\}", '')  }
                       .unique()
                       .findAll { it.endsWith("${releaseType}") }
                       .collect { it.split("-${releaseType}")[0] }
                       .findAll { it ==~ /^[0-9]+$/ }
                       .collect { it as int }.sort { -it }

  if (tags.size() == 0){
    return "1-${releaseType}"
  } else {
    return "${tags[0]+1}-${releaseType}"
  }
}

def pl = new ArrayList<StringParameterValue>()
pl.add(new StringParameterValue('NEW_RELEASE', get_next_release_version(releaseType, gitRepository).toString()))

def oldParams = build.getAction(ParametersAction.class)
if(oldParams != null) {
  newParams = oldParams.createUpdated(pl)
  build.actions.remove(oldParams)
} else {
  newParams = new ParametersAction(pl)
}

build.actions.add(newParams)