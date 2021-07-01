<template>
  <v-row justify="center">
    <v-dialog v-model="isVisible" persistent max-width="600">
      <v-card>
        <v-card-title class="headline"> Run Scenario </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-container>
              <v-row>
                <v-col>
                  <v-text-field
                    label="Number of Runs"
                    v-model.number="numberRealizations"
                    type="number"
                    :rules="[validationRulesRealizations]"
                    hide-details="auto"
                    :disabled="disableInputs"
                  >
                  </v-text-field>
                  <v-btn-toggle>
                    <v-btn-toggle v-model="numberRealizations" dense background-color="primary">
                      <v-btn small tile v-for="runCount in presetRunCounts" :key="runCount" :value="runCount">
                        {{ runCount }}
                      </v-btn>
                    </v-btn-toggle>
                  </v-btn-toggle>
                </v-col>
                <v-col>
                  <v-text-field
                    label="Seed 1"
                    v-model.number="seed1"
                    type="number"
                    hide-details="auto"
                    :disabled="disableInputs"
                  >
                  </v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    label="Seed 2"
                    v-model.number="seed2"
                    type="number"
                    hide-details="auto"
                    :disabled="disableInputs"
                  >
                  </v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
          <v-container>
            <!-- <v-progress-linear :value="currentJob.progress" class="mb-1"></v-progress-linear> -->
            <span>Job Status: {{ currentJob.status }}</span>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            v-if="!hasResults || repeatRun"
            outlined
            color="primary darken-1"
            text
            @click="runClick"
            :disabled="!canRun || isRunning"
          >
            Run
          </v-btn>
          <v-btn v-else outlined color="primary darken-1" text @click="viewResults"> View Results </v-btn>
          <v-btn outlined color="primary darken-1" text @click="isVisible = false"> Cancel </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, VModel, Watch } from 'vue-property-decorator';
import { Action, Getter, State } from 'vuex-class';
import container from '@/dependencyInjection/config';
import TYPES from '@/dependencyInjection/types';
import IJobProvider from '@/interfaces/providers/IJobProvider';
import ICreateJobRequestPayload from '@/interfaces/store/jobs/ICreateJobRequestPayload';
import JobRequest from '@/implementations/jobs/JobRequest';
import JobManager from '@/implementations/providers/JobManager';
import JobStatus from '@/enums/jobs/jobStatus';

@Component
export default class RunScenario extends Vue {
  @VModel({ default: () => false }) isVisible!: boolean;

  @Action createJobRequest!: (payload: ICreateJobRequestPayload) => void;

  @Action postCurrentJobRequest!: (jobProvider: IJobProvider) => Promise<void>;

  @Action getCurrentJobResults!: (jobProvider: IJobProvider) => Promise<void>;

  @Action UpdateJobStatus!: (status: JobStatus) => void;

  @Action UpdateJobProgress!: (progress: number) => void;

  @Action setRepeatRun!: (newValue: boolean) => void;

  @Getter canRun!: boolean;

  @Getter hasResults!: boolean;

  @State currentJob!: JobRequest;

  @State((s) => s.runSettings.repeatRun) repeatRun!: boolean;

  jobProvider = container.get<IJobProvider>(TYPES.JobProvider);

  jobManager?: JobManager;

  numberRealizations = 1;

  seed1 = 12345;

  seed2 = 678910;

  presetRunCounts = [1, 10, 100, 1000, 10000];

  isRunning = false;

  completedJobStatuses: JobStatus[] = [JobStatus.completed, JobStatus.cancelled, JobStatus.error];

  @Watch('currentJob.status')
  async onJobStatusChagned(newStatus: JobStatus): Promise<void> {
    if (this.completedJobStatuses.includes(newStatus)) {
      if (newStatus === JobStatus.completed) {
        await this.getCurrentJobResults(this.jobProvider);
      }
      await this.jobManager?.StopWatchJobProgress();
      this.isRunning = false;
    }
  }

  async runClick(): Promise<void> {
    this.isRunning = true;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const form = this.$refs.form as any;
    if (this.canRun && form.validate()) {
      const payload: ICreateJobRequestPayload = {
        jobProvider: this.jobProvider,
        numberRealizations: this.numberRealizations,
        seed1: this.seed1,
        seed2: this.seed2,
      };
      this.createJobRequest(payload);
      await this.postCurrentJobRequest(this.jobProvider);
      this.jobManager = new JobManager(this.currentJob.id, this.UpdateJobStatus, this.UpdateJobProgress);
      await this.jobManager.StartWatchJobProgress();
      if (this.repeatRun) {
        this.setRepeatRun(false);
      }
    }
  }

  get disableInputs(): boolean {
    return (this.isRunning || this.hasResults) && !this.repeatRun;
  }

  // eslint-disable-next-line class-methods-use-this
  validationRulesRealizations(value: number): boolean | string {
    if (!value) {
      return 'Value is required';
    }
    if (value < 1) {
      return 'Value must be at least 1';
    }
    if (value > 10000) {
      return 'Value must be less than 10000';
    }
    if (value % 1 !== 0) {
      return 'Value must be a whole number';
    }
    return true;
  }

  viewResults(): void {
    this.$router.push({ name: 'viewResults' });
    this.isVisible = false;
  }
}
</script>

<style lang="scss" scoped></style>
