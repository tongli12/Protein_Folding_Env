from agents.basic_policy import Policy
import os


class Random(Policy):
    def __init__(self, model, env, args=None, device='cpu'):
        super(Random, self).__init__(model, env, args, device)

        self.ppo_epochs = 4
        self.max_steps = args.max_steps
        self.mini_batch_size = args.batch_size
        self.clip_param = self.args.clip_param
        self.update_frequency = self.args.update_frequency

    def train(self):

        action1 = []
        action2 = []
        mc_keep = []

        step = 0
        state = self.env.reset()

        while step < self.max_steps:

            next_state, reward, done, score_before_mc, score_after_mc, rmsd, keep = self.env.step()

            state = next_state
            step += 1

            # Keep track the result
            self.tracker.insert((self.env.pose.clone(), score_after_mc, rmsd))

            if step % self.args.log_frequency == 0:

                print(f'frame_idx: {step}   Rosetta score: {score_after_mc}   RMSD: {rmsd}')
                self.writer.add_scalar('score_before_mc', score_before_mc, step)
                self.writer.add_scalar('score_after_mc', score_after_mc, step)
                self.writer.add_scalar('rmsd', rmsd, step)
                self.writer.add_scalar('lowest', self.tracker.lowest, step)
                self.writer.add_scalar('highest', self.tracker.highest, step)

            if step % self.args.save_frequency == 0:

                self.tracker.save(self.args.gen_path, self.task)
                # self.env.pose.dump_pdb(os.path.join(self.args.gen_path, self.task + '_traj_' + str(step) + '.pdb'))
